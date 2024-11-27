# How to add a new processing step

ISSA pipeline is designed to be open to extension. Adding a new document processing requires a few steps.

We anticipate that a new process would be one of three types:

- performing indexation, i.e. associating terms with the entire text
- performing named entity recognition (NER), i.e. associating entities with an exact word or phrase in the text
- performing something else

In any case, the process would be is very similar. For example, the use case specific  _pyclinrec_ NER can serve as a template for adding a new step.

## Identify the input and output types and locations

Possible inputs:

- metadata: global tsv or separate json documents
- full document text (json)
- results of other processing steps (json)

Possible outputs:

- json files one per document (preferred) in the same folder
- tsv file

Update the *env.sh* in the corresponding instance [config](../config/) directory with the relative path of the output folder.

For example:

```bash
export REL_NEW_NER=annotation/new_ner      # New annotations 
```

>:point_right: the *env.sh* contains variables that are used across ISSA pipeline and environment

## Implementation

If a new processing step is developed in Python preferably:

- update the *config.py* in the corresponding instance [config](../config/) directory  with a new configuration class derived from the *cfg_annotation* class specifying input-output locations and other configurable parameters (follow the example of a similar existing steps)
- take advantage of logging, file access and dictionary utility functions implemented in [util.py](./util.py)
- if a new step can be classified as [NER(./ner/)] or [indexing](./indexing/) then put its code into a respective directory, otherwise create a new folder for it.

If a new step is not a Python code make sure that the output files are put into a location defined in *env.sh*.

## Mapping new output to RDF

The transformation of JSON|TSV output into Turtle formatted RDF happens in two steps: loading to MongoDB and mapping fields from a MongoDB collection to Turtle using xR2RML mapping language.

#### MongoDB

In [mongo](./morph-xr2rml/mongo/) directory there are scripts that assist an easy integration.

- for JSON output add a line to the [run_import.sh](./morph-xr2rml/mongo//run-import.sh), where
  - _new-collection-name_ is an arbitrary new collection name
  - _document-id_ - a name of json element that would be a key of the collection (typically paper_id)
  - _relative-path-to-output-directory_ - output path defined in *env.sh* (see above)
  - _post-load-script.js_ - optional custom script that executes after the load of the target collection and can include aggregation or filtering of unnecessary elements

```bash
docker exec -w $WDIR $CONTAINER \
           /bin/bash ./import-json-dir.sh \
                      $DB <new-collection-name> <document_id> \
                      $IDIR//<relative-path-to-output-directory> \
                      $SDIR/<post-load-script.js>   &>> $log

```

- for tsv output add a line like the following, where
  - _document-id_ is a column that becomes a collection key
  - _file-name.tsv_ is the name of a file to load

```bash
docker exec -w $WDIR $CONTAINER \
            /bin/bash ./import-file.sh \
                      $IDIR/<new-tsv-file.tsv> tsv \
                      $DB <new-collection-name> <document_id> \
                      $SDIR/<post-load-script.js>   &>> $log

```

The only work besides adding a line to the script would be to develop an __optional__ post-load script that requires some familiarity with [MongoDB scripting](https://www.mongodb.com/docs/mongodb-shell/write-scripts/).

#### xR2RML

In [xR2RML](./morph-xr2rml/xR2RML) directory there are tools that transform MongoDB collections into an RDF using the R2RML language templates. The transformation templates for the existing pipeline are also stored here.

For new kind of data, a new transformation template has to be added. The easiest way to develop such template is to choose an existing one whose input resembles new data and adapt.

>:point_right: to make the RDF files of manageable size the named entities annotations can be split into separate files for title, abstract and body text.

New data should be entered into the graph with its provenance information. At minimum with `rdfs:isDefinedBy` and `prov:wasAttributedTo`. As in the example below:

```Turtle
    # Provenance
    rr:predicateObjectMap [
        rr:predicate rdfs:isDefinedBy;
        rr:objectMap [ rr:constant issa:{{dataset}}; rr:termType rr:IRI ];
    ];
    rr:predicateObjectMap [
        rr:predicate prov:wasAttributedTo;
        rr:objectMap [ rr:constant issa:Documentalist; rr:termType rr:IRI ];
    ]
```

A new step has to be defined as an _Agent_ according to the [PROV-O](https://www.w3.org/TR/prov-o/) ontology, it could be _Person_, _Organization_, or _SoftwareAgent_. A new _agent has to be described in the [provenance.ttl](https://github.com/issa-project/issa-pipeline/blob/main/dataset/provenance.ttl) file.

After the template is developed add a line to the [run-transformation.sh](./morph-xr2rml/xR2RML/run-transformation.sh) script:

- for non-annotation data
  - _new-collection-name_ is the same new collection name
  - _new-xr2rml_template.tpl.ttl_ - developed template
  - _new-rdf-output.ttl_ - target output

```bash
docker_exec "Generate new output..." \
            <new-xr2rml_template.tpl.ttl> \
            <new-rdf-output.ttl> \
            <new-collection-name>
```

- for NE annotations split by article part
  - _article-part_ is an article part such as title, abstract or body_text

```bash
./run_xr2rml_annotation.sh $DS article-part new-collection-name \
                new-xr2rml_template.tpl.ttl \
                $ODIR/new-rdf-output.ttl
docker_exec_multipart "Generate new output..." \
                      <new-xr2rml_template.tpl.ttl> \
                      <new-rdf-output-part.ttl> \
                      <new-collection-name> 
```
>:point_right: The word **part** in the name of the output file is important. It will be substituted by the actual annotated part such as title, abstract or body_text. 

### Publishing new RDF in Virtuoso triple store

Identify a named graph where new triples will be uploaded. Most likely it has to be a new graph. Use the existing naming convention to name a graph.

Determine if this graph has to be fully or incrementally updated (most likely the second).

Modify [import-all.isql](./virtuoso/import-all.isql) script. Add a line:

```bash
ld_dir ('$u{IDIR}', 'new-rdf-output*.ttl',    $u{namespace}graph/new-graph-name);
```

In the case of full update add line at the top of the script:

```bash
SPARQL CLEAR GRAPH  <$u{namespace}graph/new-graph-name>;
```

>:point_right: punctuation is important. Make sure that angle brackets and quotation marks are correctly applied.

## Integration into pipeline

If a new processing step performs indexation (e.g. associating terms with entire text) add an execution call to the [3_index_articles.sh](./3_index_articles.sh) script.

If a processing step is named entity recognition (NER) (eg. associating entities with an exact word or phrase) add a call to [4_annotate_articles](./4_annotate_articles.sh) script.

If non of the above  then a call can be added to [run-pipeline.sh](./run-pipeline.sh).

>:point_right: Make sure that a new step is called after the pre-requisite steps are called.
