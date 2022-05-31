# ISSA Pipeline

ISSA pipeline consists of steps that flow document data from obtaining their metadata trough the process of text extraction and annotation to the publication as a Knowledge Graph.

<img src="../doc/pipeline_details.png" width="900" />

To adapt this pipeline to a differnt document repository only the metadata step and json-RDF mappings have to be modified.

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
- metadata json according to the [schema](../doc/ISSA_json_schema.txt) 
- files containing pdf URLs for the full text extraction in the next step
- (optionally) text files with title and abstract text for trainnig the indexing models
- (optionally) tsv files with descriptors URIs and lables also for trainnig the indexing models 

### Full text extraction
Typically the document repositories contain text of title and possibly abstract of a document. For some use cases that may be enough to annotate a document. In this case this step can be skipped.
In other cases an attempt to extract the text from PDF of a document is nesessary. We use [Grobid](https://grobid.readthedocs.io/en/latest/Introduction/) machine learning library for extracting, parsing and re-structuring raw documents.  

NB: The text extraction is not always possible. For example, if a pdf file is a scan of a document. 
NB: The extracted text is not very clean and can contain misalign and missing parts of a text. To compencate for this, if title and abstract are available from the metadata they can be coalesced into one text.   

On this step for each pdf URL file created from the metadata:
- download pdf
- extract text 
- (optionally) coalesce extracted text with metadata 

The follwing intermediate files are produced at this point:
- full text json according to the [schema](../doc/ISSA_json_schema.txt) 
- (optionally) coaleced json 
- (optionally) XML/TEI encoded documents output by Grobid

NB: A massive download of pdf documents from an HTTP server may cause problems for a host and a client. To facilitate a succesful download time spacing option is provided. However, during the waiting time the Grobid extraction can take place for efficiency. Also caching of the pdf files is recommended and provided and can be either in a separate directory or in the dataset directories {review}.

 


