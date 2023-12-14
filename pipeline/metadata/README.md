## Metadata 

This set of Python scripts implements the interface between the original document corpus repository and ISSA and creates a foundation for further processing. The three steps to create an ISSA-processable dataset:

- download corpus metadata
- process corpus metadata
- output ISSA documents' metadata 

## Download

The assumption is that an original data source has an API that provides document corpus metadata. In the use cases of Agritrop and HAL the API is [OAI-PMH](https://www.openarchives.org/pmh/). For another document corpus these scripts have to be adjusted:

- in case if another document corpus also has OAI-PMH it might be only necessary to adjust field mappings in the instance's config.py.
- in case of a different API downloading code has to be rewritten.
- in case the metadata file is already provided then the downloading step can be omitted.

Raw metadata should be generated at this point in TSV format.

## Process

Typically, the original data has to be somehow cleaned and/or filtered. The main document identifier *paper_id* has to be created. Some fields in the raw data  may have to be transformed to the ISSA schema with additional processing. The mapping is done in the instance's config.py by creating a dictionary that maps an input and output field and a transformation function(s).

 A set of generic transformations is provided in [process_corpus_metadata.py](process_corpus_metadata.py) to facilitate the necessary processing. However, a corpus may have a unique processing step that can also be defined in config.py.

 The following output fields can be mapped that do not require any other change in the ISSA pipeline:

- *paper_id* - a unique document identifier
- *title* - a document title
- *abstract* - a document abstract
- *authors* - a document authors
- *publication* - a document publication venue
- *year* - a document publication year
- *language* - a document 2-letter [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) language code
- *language bib* - a document bibliographic 3-letter [ISO-639-2](https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes) language code

- *url* - a document source URL
- *pdf_url* - a document PDF URL
- *doi* - a document DOI
- *same_as* - other links associated with the document

- *classes* - a document classe URIs according to [FaBiO](https://sparontologies.github.io/fabio/current/fabio.html), [BIBO](https://www.dublincore.org/specifications/bibo/bibo/) , [EPrints](https://www.eprints.org/ontology/?format=RDF), or other ontology
- *license* - a document license URI e.g. [Creative Commons](https://creativecommons.org/licenses/)
- *access_rights* - a document access level URI e.g. [OpenAIRE Access Level](https://guidelines.openaire.eu/en/latest/literature/field_accesslevel.html)
- *rights* - rights that are not addressed by *license* and *access_rights* fields such as copyright statements

For thematic descriptors and domains that come with metadata it is necessary to create a column with URIs and a column with corresponding labels in the same order. The labels can be either extracted from the metadata or can be queried from the current version of domain-specific descriptor vocabulary. The labels' language has to correspond to the document language. 

If the author's keywords are provided by the corpus it is necessary to create a column with keywords and a column with corresponding language codes in the same order.

- *descriptors_uris* - a document descriptors URIs
- *descriptors_labels* - a document descriptors labels
- *domain_uris* - a document domain URIs
- *domain_labels* - a document domain labels
- *keywords* - a document keywords
- *keywords_lang* - a document keywords language

The metadata may contain text for titles and abstracts. For better annotation results the language of the text is automatically determined. However, language detection is optional and can be configured._

If the text field language is detected the additional fields  are created:

- *title_lang* - a document title language
- *abstract_lang* - a document abstract language
- *title_lang_score* - a document title language detection score
- *abstract_lang_score* - a document abstract language detection score

>:point_right: Language detection by cld2 package does not work on Windows.

Processed data file in TSV format should be generated at this point.

## Initialize data repository

The idea is that the further processing of the document corpus will rely on the presence of certain files in the dataset repository and should be a document corpus agnostic. To facilitate this

- we create a specific folder structure that is defined in the [env.sh](../env.sh) and visible to all steps of the pipeline, 
- we name files generated per document with *<paper_id>.<ext>* pattern.

If a document corpus is updated on a regular basis each update of the metadata and other corresponding files are stored in the dated folders.

>:point_right: It is important to date folders so the latest would come at the top of the sorted in descending order list.

Here is an example of the repository structure:
```
├── agritrop
|   ├── dataset-1-0
|   │   ├── 20220202
|   │   │   ├── annotation
|   │   │   │   ├── dbpedia
|   │   │   │   ├── geonames
|   │   │   │   └── wikidata
|   │   │   ├── indexing
|   │   │   │   ├── en
|   │   │   │   └── fr
|   │   │   ├── json
|   │   │   │   ├── coalesced
|   │   │   │   ├── fulltext
|   │   │   │   └── metadata
|   │   │   ├── labels
|   │   │   ├── pdf
|   │   │   ├── rdf
|   │   │   ├── txt
|   │   │   └── xml
|   ├── pdf_cache
|   │   └── unreadable
|   └── training
|       ├── en
|       │   ├── test
|       │   └── train
|       └── fr
|           ├── test
|           └── train
```

At this point the following output is generated:

- single metadata.tsv file in the datestamped directory
- <paper_id>.json containing titles, abstracts, detected languages according to the [schema](../../doc/ISSA_json_schema.txt) in /json/metadata directory
- <paper_id>.url files containing PDF URLs to be used to download actual PDF files in /pdf directory
- (optionally) <paper_id>.tsv files with descriptors' URIs and labels to be used for training indexing models in /labels directory
- (optionally) <paper_id>.txt files with text from metadata that can be used for training indexing models in case if PDF is not available in /txt directory

>:point_right: The directories in the example above can be reconfigured in the instance env.sh or [env.sh](../../env.sh)
