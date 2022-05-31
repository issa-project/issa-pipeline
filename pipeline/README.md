# ISSA Pipeline

ISSA pipeline consists of steps that flow document data from obtaining their metadata trough the process of text extraction and annotation to the publication as a Knowledge Graph.

<img src="doc/pipeline_details.png" width="700" />

To adapt this pipeline to a differnt document repository only the downloadin metadata step has to be modified.

## Source Code

ISSA pipeline's source code is a cmbination of Python scripts for data processing and Linux bash scripts for data flow. 

## Configuration

There are two levels of configuration that define the data flow and processing options:
 - environnment and data loaction are defined in [env.sh](../env.sh)
 - processing options for Python scripts are defined in [config.py](config.py)

## Pipeline Step by Step
### Metadata
Typically the documents in the repositories are accompanied by their metadata which can inculde title, authors, pdf URL, thematic descriptors, etc. 
The metadata is typically come in a tabular format and can be obtained through the repository's API. In the use case of Agritrop the metadata is obtained through [OAI-PMH](https://www.openarchives.org/pmh/) protocol from the [Open Repository of CIRAD publications](https://agritrop.cirad.fr/). A mechanism of mapping API output to the table columns is provided.

The most relevant metadata fields for ISSA pipeline would be:
- id
- title
- abstract
- pdf URL
- thematic descriptors
After cleaning and processing metadata (which would be different for each use case scenario) the following intermediate files are produced:
- metadata json according to a [schema](metadata/ISSA_json_schema.txt) 
- files containing pdf URLs for the full text extraction in the next step
- (optional) text files with title and abstract text for trainnig the indexing models
- (optional) tsv files with descriptors URIs and lables also for trainnig the indexing models 

### Full text extraction
