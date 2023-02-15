# How to add a new document processing step

ISSA pipeline is designed to be open to extension. Adding a new document processing requires a few steps.

We anticipate that a new process would be one of three types:

- performing indexation, i.e. associating terms with entire text
- performing named entity recognition (NER), i.e. associating entities with an exact word or phrase in the text
- performing something else  

In any case the process would be is very similar. For example the use case specific  _pyclinrec_ NER was added to the pipeline last and can serve as a template for adding a new step.

## Identify the input and output types and locations

Possible inputs:

- metadata (tsv)
- full document text (json)
- results of other processing steps (json)

Possible outputs:

- json files one per document (preferred) in the same folder
- tsv file

Update the [env.sh](https://github.com/issa-project/issa-pipeline/blob/main/env.sh) with the relative path of the output folder. for example

```bash
export REL_NEW_NER=annotation/new_ner      # New annotations 
```

>:point_right: the  [env.sh](https://github.com/issa-project/issa-pipeline/blob/main/env.sh) contains variables that are used across ISSA pipeline and environment

## Implementation

If a new processing step is developed in Python preferably:

- update the [config.py](https://github.com/issa-project/issa-pipeline/blob/main/pipeline/config.py) file with a new configuration class derived from cfg_annotation class specifying input-output locations and other configurable parameters  (follow the example of existing steps)
- take advantage of logging, file access and dictionary utility functions implemented in [util.py](https://github.com/issa-project/issa-pipeline/blob/main/pipeline/util.py)
- if a new step can be classified as NER or indexing than put its code to a respective folder, otherwise create a new folder for it.

If a new step is not a Python code make sure that the output files are put into a location defined in [env.sh](https://github.com/issa-project/issa-pipeline/blob/main/env.sh).

## Mapping new output to RDF

The transformation of json|tsv output into Turtle formatted RDF happens in two steps: loading to MongoDB and mapping fields from a MongoDB collection to Turtle using xR2RML mapping language.

### MongoDB

In [mongodb](https://github.com/issa-project/issa-pipeline/tree/main/pipeline/mongo) directory there are scripts that assist an easy integration.

- for json output add a line to the [run_import.sh](https://github.com/issa-project/issa-pipeline/blob/main/pipeline/mongo/run-import.sh), where
  - _new-collection-name_ is an arbitrary new collection name
  - _document-id_ - name of json element that would be a key of the collection (typically paper_id)
  - _relative-path-to-output-directory_ - output path stored in [env.sh](https://github.com/issa-project/issa-pipeline/blob/main/env.sh)
  - _post-load-script.js_ - optional custom script that executes after the load of the target collection and can include aggregation or filtering of unnecessary elements

```bash
docker exec -w $WDIR $CONTAINER \
           ./import-json-dir.sh \
           $DB new-collection-name document-id \
           $IDIR/$relative-path-to-output-directory \
           post-load-script.js &>> $log

```

- for tsv output add a line like following, where
  - _document-id_ is a column that becomes a collection key
  - _file-name.tsv_ is the name of a file to load

```bash
docker exec -w $WDIR $CONTAINER \
            ./import-tsv-file.sh $DB new-collection-name document-id \
            $IDIR/$file-name.tsv \
            post-load-script.js &>> $log
```

The only work besides adding a line to a script would be to develop an __optional__ post-load script that requires some familiarity with [MongoDB scripting](https://www.mongodb.com/docs/mongodb-shell/write-scripts/).

### xR2RML

In [xR2RML](https://github.com/issa-project/issa-pipeline/tree/main/pipeline/xR2RML) directory there are tools that transform MongoDB collections into an RDF using the R2RML language templates. The transformation templates for existing pipeline are also stored here.

For a new data a new transformation template has to be added. The easiest way to develop such template is to choose an existing one whose input resembles new data and adapt. More details about the transformation tool can be found [here](https://github.com/issa-project/issa-pipeline/tree/main/pipeline/xR2RML).

>:point_right: to make the RDF files of manageable size the named entities annotations can be split into separate files for title, abstract and body text.

New data should be entered to the graph with its provenance information. At minimum with `rdfs:isDefinedBy` and `prov:wasAttributedTo`. As in the example below:

```Turtle
    # Provenance
    rr:predicateObjectMap [
        rr:predicate rdfs:isDefinedBy;
        rr:objectMap [ rr:constant issa:{{dataset}}; rr:termType rr:IRI ];
    ];
    rr:predicateObjectMap [
        rr:predicate prov:wasAttributedTo;
        rr:objectMap [ rr:constant issa:AgritropDocumentalist; rr:termType rr:IRI ];
    ]
```

A new step has to be defined as an _Agent_ according to the [prov-o](https://www.w3.org/TR/prov-o/) ontology, it could be _Person_, _Organization_, or _SoftwareAgent_. A new _agent has to be described in the [provenance.ttl](https://github.com/issa-project/issa-pipeline/blob/main/dataset/provenance.ttl) file.

After the template is developed add a line to the [run-transformation.sh](https://github.com/issa-project/issa-pipeline/blob/main/pipeline/xR2RML/run-transformation.sh) script:

- for non-annotation data
  - _new-collection-name_ is the same new collection name
  - _new-xr2rml_template.tpl.ttl_ - developed template
  - _new-rdf-output.ttl_ - target output

```bash
./run_xr2rml.sh $DS new-collection-name \
                new-xr2rml_template.tpl.ttl \
                $ODIR/new-rdf-output.ttl
```

- for NE annotations split by article part
  - _article-part_ is an article part such as title, abstract or body_text

```bash
./run_xr2rml_annotation.sh $DS article-part new-collection-name \
                new-xr2rml_template.tpl.ttl \
                $ODIR/new-rdf-output.ttl
```

### Virtuoso

Identify a graph where new triples will be uploaded. Most likely it has to be a new graph. Use the existing naming convention to name a graph.

Determine if this graph has to be fully or incrementally updated (most likely the second).

Modify [import-all.isql](https://github.com/issa-project/issa-pipeline/blob/main/pipeline/virtuoso/import-all.isql) script. Add a line:

```bash
ld_dir ('$ARGV[$I]', 'new-rdf-output-*.ttl', 'new-graph-name');
```

In the case of full update add line at the top of the script:

```bash
SPARQL CLEAR GRAPH  <new-graph-name>;
```

>:point_right: punctuation is important. MAke sure that angle brackets and quotation marks are correctly applied.

## Integration into pipeline

If a new processing step performs indexation (e.g. associating terms with entire text) add an execution call to the [3_index_articles.sh](https://github.com/issa-project/issa-pipeline/blob/main/pipeline/3_index_articles.sh) script.

If a processing step is named entity recognition (NER) (eg. associating entities with an exact word or phrase) add a call to [4_annotate_articles](https://github.com/issa-project/issa-pipeline/blob/main/pipeline/4_annotate_articles.sh) script.

If non of the above  then a call can be added to [run-pipeline.sh](https://github.com/issa-project/issa-pipeline/blob/main/pipeline/run-pipeline.sh).

>:point_right: Make sure that a new step is called after the pre-requisite steps are called.
