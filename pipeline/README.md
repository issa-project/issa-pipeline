# ISSA Pipeline

ISSA pipeline consists of steps that flow document data from obtaining their metadata through the process of text extraction and annotation to the publication as a Knowledge Graph.

<img src="../doc/pipeline_details.png" width="900" />

To adapt this pipeline to a different document repository only the metadata step and JSON-RDF mappings have to be modified.

## Source Code
ISSA pipeline's source code is a combination of Python scripts for data processing and Linux bash scripts for data flow and tools integration. 

## Configuration
There are two levels of configuration that define the data flow and processing options:
 - environment and data loaction are defined in [env.sh](../env.sh)
 - processing options for Python scripts are defined in [config.py](config.py)
 
## Runing pipeline
After configuring the pipeline it can be run manually step-by-step by running numbered scripts in this directory or by invoking [run-pipeline.sh](run-pipeline.sh) to run the entire pipeline automatically.

We'd recommend to run the pipeline manually for the first time to be able to catch potential configuration issues earlier. Updates can be run automatically. 

Each step of the pipeline outputs a log file that would be stored in *logs* directory. 
 
## Data Updates
Initial run of ISSA pipeline creates dataset file repository, intermedidate storage and resulting KG in the Virtuoso triple store. 
After that ISSA pipeline can be run periodically to incrementally update the KG with new documents data from the source.
 
On the update metadata will be reprocessed in full to account for the updates in the source. However, the text extraction and annotation would be performed on the new documents only. The triple store will be updated accordingly. 
The data is stored in the dataset directory and each update (including initial load) is saved in the sub-directory with its date.

## Pipeline Step-by-Step
### Download Metadata
Typically, documents in the repositories are accompanied by their metadata which can include title, authors, PDF URL, thematic descriptors, etc. 
The metadata is typically come in a tabular format and can be obtained through the repository's API. 
In the use case of Agritrop the metadata is obtained through [OAI-PMH](https://www.openarchives.org/pmh/) protocol from the [Open Repository of CIRAD publications](https://agritrop.cirad.fr/). A mechanism of mapping API output to the table columns is provided.

The most relevant metadata fields for ISSA pipeline would be:
- id
- title
- abstract
- PDF URL
- thematic descriptors

After pre-processing metadata (which would be different for each use case scenario) the following output is generated:
- metadata TSV file
- metadata text (titles, abstracts) JSON according to the [schema](../doc/ISSA_json_schema.txt) 
- <id>.url files containing PDF URLs to be used in the next step
- (optionally) TSV files with descriptors URIs and labels also for training the indexing models 

Scripts are provided in directory [metadata](./metadata/).

### Full text extraction
Typically, document repositories contain text of title and possibly abstract of a document in the metadata. For some use cases that may be enough to annotate a document. In this case this step can be skipped.
In other cases an attempt to extract the text from PDF of a document is necessary. We use [GROBID (2008-2022)](https://github.com/kermitt2/grobid) machine learning library for extracting, parsing and re-structuring raw documents.  

On this step for each PDF URL file created from the metadata:
- download PDF
- extract text 
- (optionally) coalesce extracted text with metadata 

The following intermediate files are produced at this point:
- extracted text JSON according to the [schema](../doc/ISSA_json_schema.txt) 
- (optionally) extracted text coalesced with metadata JSON 
- (optionally) XML/TEI encoded documents output by Grobid (useful for debugging purposes)

>:point_right: The text extraction is not always possible. For example, if a PDF file is a scan of a document.   
>:point_right: The extracted text is not always "clean" and can contain misaligned and missing parts of a text. To compensate for this, if title and/or abstract are available from the metadata they can be coalesced with extracted text into one JSON document.   
>:point_right: A massive download of PDF documents from an HTTP server may cause problems for a host and a client. Caching of the PDF files is recommended and mechanisms are provided in the pipeline.

Scripts are provided in directory [fulltext](./fulltext/).

### Thematic Indexing 
In ISSA pipeline thematic indexing refers to an automatic annotation of a document with thematic descriptors. Thematic descriptors are keywords (typically 5 or 6) or expressions that characterize an article as a whole and that are linked to a domain specific vocabulary. For some repositories human documentalists manually annotate articles with descriptors, which yields accurate annotations but is time consuming.   

In the Agritrop use case the thematic descriptors are chosen from the [AGROVOC](https://www.fao.org/agrovoc/) vocabulary. Large corpus of the existing documents is already annotated by documentalist which allows to train a specialized supervised classification model to automatically assign thematic descriptors to publications. 

ISSA pipeline includes such a classification system through the integration of [Annif](https://annif.org/) [2], a framework developed by the National Library of Finland. Read more on Annif model selection and training [here](../training/).

On this step from document text JSON files created in the previous step:
- create plain text files per Annif framework's requirement
- separate text file by language 
- extract thematic descriptors by applying classification models for each language

The following files are output at this step:
- text files
- JSON files with thematic descriptors according to the following schema
```
{'paper_id' <str>, 
 'model': <str>, 
 'language': <str>,  	
 'subjects' : [{'uri': <str>,
		'label': <str>,
		'conf_score': <number>;,
		'rank': <number>}]
}
```
>:point_right: The classification models are trained separately for each language.
	
Scripts are provided in directory [indexing](./indexing/).

### Named Entity Recognition
ISSA pipeline relies on tools to identify, disambiguate and link named entities from the documents:
- [DBpedia Spotlight](https://www.dbpedia-spotlight.org/)
- [Entity-fishing](https://github.com/kermitt2/entity-fishing)
- identifies geographic entities by looking for [GeoNames](https://www.geonames.org/ontology/documentation.html) mappings in the recognised Wikidata concepts.

On this step for each document's JSON file the pipeline invokes each of these tools for each part of a document (title, abstract, body). The tool's responses are encapsulated into a simple schema:
```
{'paper_id' <str>, 
 'title':      { DBPedia Spotlight or Entity-fishing response }, 
 'abstract':   { DBPedia Spotlight or Entity-fishing response }, 
 'body_text' : { DBPedia Spotlight or Entity-fishing response }, 
}
```
The following output files are generated: 
- JSON files with DBPedia named entities annotations
- JSON files with Wikidata named entities annotations
- JSON files with GeoNames named entities annotations

>:point_right: The tools' responses are verbous and contain the full annotated text. The options to remove the text is provided to save the space.   
>:point_right: GeoNames named entities are saved in the same way as Wikidata with an addition of GeoNamesID field.

Scripts are provided in directory [ner](./ner/).

### Transformation to RDF
The transformation of the metadata, document text, thematic descriptors and annotations is carried out using [Morph-xR2RML](https://github.com/frmichel/morph-xr2rml/), an implementation of the [xR2RML mapping language](http://i3s.unice.fr/~fmichel/xr2rml_specification.html) [1] for MongoDB databases.

The previosly collected data is 
- imported to the [dockerised MongoDB](https://hub.docker.com/_/mongo) 
- transformed into RDF format following the provided mapping templates.

The output of this step is a set of 
- Turtle (ttl) files with document metadata & text
- Turtle (ttl) files with thematic descriptots
- Turtle (ttl) files with named entities

>:point_right: Only metadata mappings have to be adapted for a different dataset. 
	
Scripts are provided in directories [mongo](./mongo/) and [xR2RML](./xR2RML/).

### Uploading to Virtuoso Triple Store
RDF files generated at the previous stage are imported into a [dockerised Virtuoso OS instance](https://hub.docker.com/r/openlink/virtuoso-opensource-7/) as separate named graphs. 

| Data type                            | Named Graph                                           |
|--------------------------------------|-------------------------------------------------------|
| Metadata                             | http://data-issa.cirad.fr/graph/articles              |
| Annotated text                       | http://data-issa.cirad.fr/graph/articles/text         |
| Human-validated thematic descriptors | http://data-issa.cirad.fr/graph/thematic-descriptors  |
| Annif-generated thematic descriptors | http://data-issa.cirad.fr/graph/annif-descriptors     |
| DBpedia annotations                  | http://data-issa.cirad.fr/graph/dbpedia-spotlight-nes |
| Wikidata annotations                 | http://data-issa.cirad.fr/graph/entity-fishing-nes    |
| GeoNames annoatations                | http://data-issa.cirad.fr/graph/geographic-nes        |

Scripts are provided in directory [virtuoso](./virtuoso/).

## References

[1] F. Michel, L. Djimenou, C. Faron-Zucker, and J. Montagnat. Translation of Relational and Non-Relational Databases into RDF with xR2RML.
In Proceedings of the *11th International Confenrence on Web Information Systems and Technologies (WEBIST 2015)*, Lisbon, Portugal, 2015.

[2] O. Suominen, J. Inkinen, T. Virolainen, M. Fürneisen,  B. P. Kinoshita, S. Veldhoen, M. Sjöberg, P. Zumstein, R. Neatherway, & M Lehtinen (2022). Annif (Version 0.58.0-dev) [Computer software]. https://doi.org/10.5281/zenodo.2578948
	
