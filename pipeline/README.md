# ISSA Pipeline

ISSA pipeline consists of steps that flow document data from obtaining their metadata through the process of text extraction and annotation to the publication as a Knowledge Graph.

<img src="../doc/pipeline_details.png" width="900" />

To adapt this pipeline to a different document repository only the metadata step and json-RDF mappings have to be modified.

## Source Code

ISSA pipeline's source code is a combination of Python scripts for data processing and Linux bash scripts for data flow and tools integration. 

## Configuration

There are two levels of configuration that define the data flow and processing options:
 - environment and data loaction are defined in [env.sh](../env.sh)
 - processing options for Python scripts are defined in [config.py](config.py)

## Pipeline Step by Step
### Metadata
Typically, documents in the repositories are accompanied by their metadata which can include title, authors, pdf URL, thematic descriptors, etc. 
The metadata is typically come in a tabular format and can be obtained through the repository's API. In the use case of Agritrop the metadata is obtained through [OAI-PMH](https://www.openarchives.org/pmh/) protocol from the [Open Repository of CIRAD publications](https://agritrop.cirad.fr/). A mechanism of mapping API output to the table columns is provided.

The most relevant metadata fields for ISSA pipeline would be:
- id
- title
- abstract
- pdf URL
- thematic descriptors

After cleaning and processing metadata (which would be different for each use case scenario) the following intermediate files are produced:
- metadata json according to the [schema](../doc/ISSA_json_schema.txt) 
- files containing pdf URLs for the full text extraction in the next step
- (optionally) text files with title and abstract text for training the indexing models
- (optionally) tsv files with descriptors URIs and labels also for training the indexing models 

### Full text extraction
Typically, document repositories contain text of title and possibly abstract of a document in the metadata. For some use cases that may be enough to annotate a document. In this case this step can be skipped.
In other cases an attempt to extract the text from PDF of a document is necessary. We use [Grobid](https://grobid.readthedocs.io/en/latest/Introduction/) machine learning library for extracting, parsing and re-structuring raw documents.  

NB: The text extraction is not always possible. For example, if a pdf file is a scan of a document. 

NB: The extracted text is not always "clean" and can contain misaligned and missing parts of a text. To compensate for this, if title and/or abstract are available from the metadata they can be coalesced with extracted text into one json document.   

On this step for each pdf URL file created from the metadata:
- download pdf
- extract text 
- (optionally) coalesce extracted text with metadata 

The following intermediate files are produced at this point:
- full text json according to the [schema](../doc/ISSA_json_schema.txt) 
- (optionally) coalesced json 
- (optionally) XML/TEI encoded documents output by Grobid

A massive download of pdf documents from an HTTP server may cause problems for a host and a client. To mitigate a potential issue, time spacing between downloads is provided. However, during the waiting time the Grobid extraction can still take place for efficiency. 
Caching of the pdf files is recommended and mechanisms are provided in the pipeline.

### Indexing
In ISSA pipeline indexing refers to an automatic annotation of a document with thematic descriptors. Thematic descriptors are keywords (typically 5 or 6) or expressions that characterize an article as a whole and that are linked to a domain specific vocabulary. For some repositories human documentalists manually annotate articles with descriptors, which yields accurate annotations but is time consuming.   

In the Agritrop use case the thematic descriptors are chosen from the [AGROVOC](https://www.fao.org/agrovoc/) vocabulary. Large corpus of the existing documents is already annotated by documentalist which allows to train a specialized supervised classification model to automatically assign thematic descriptors to publications. 

The ISSA pipeline includes such a classification system through the integration of [Annif](https://annif.org/), a framework developed by the National Library of Finland. 

Before applying a classification model to documents, this model should be trained. Read more on Annif model selection and training [here](../training/).

NB: The classification models are created separately for each language.

On this step for json files created in the previous step:
- create plain text files per Annif framework's requirement
- separate text file by language 
- extract thematic descriptors by applying classification models for each language

The following intermediate files are output at this step:
- text files
- json files with thematic descriptors according to the following schema

    {'paper_id' : <str>,
     'model': <str>,
     'language': <str>,
     'subjects' : [{'uri': <str>,
				  'label': <str>,
				   'conf_score': <number>,
				   'rank': <number>}]
    }



