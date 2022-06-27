# Metadata processing

This set of scripts implements the interface between the original data and ISSA and create a foundation for further processing. The three steps to create ISSA processable dataset:
- download corpus metadata 
- process corpus medata
- output ISSA dataset metadata

## Download
The assumption is that an original data source has an API that provides document corpus metadata. In the use case of Agritrop the API is [OAI-PMH](https://www.openarchives.org/pmh/). For another document corpus these scripts have to be adjusted:
- in case if another document corpus also has OAI-PMH it might be only nesessary to adjust field mappings in the [config.py](../config.py).
- in case of a different API some code adjustments would be nesessary.
- in case if the metadata file is already provided then the downloading step can be omitted.

Raw datafile should be generated at this point.

## Processing
Typically the original data has to be somehow cleaned and/or filtered. A set of functions can by piped together to facilitate the nesessary processing. 
The main document identifier *paper_id* has to be created.
For thematic descriptors that come with metadata it is nesessary to create a column *decriptors-uris* in the metadata that lists a document descriptors URIs and a column for corersponding labels *descriptors_lables* in the same order. The labels can be either extracted from the metadata or can be queried from the current version of domain-specific descriptor vocabulary. The labels' language has to correspond to the document language. 
Metadata may contain text for title and abstract. For better annotation result the language of the text is automatically determined. However language detection is optional and can be configured.

>:point_right: Language detection does not work on Windows and has to be turned off.        

Processed datafile should be generated at this point.

## Create data repository
The idea is that for the further processing of the document corpus will rely on the presence of certain files in the dataset repository and document corpus agnostic. To facilitate this
- we cretae a specific folder structure that is defined in the [env.sh](../env.sh) and visible to all steps of the pipeline 
- we name the files generated per document with *<paper_id>.<ext>* pattern.   

If a document corpus is updated on a regular basis each update of the metadata and other corresponding files are stored in the dated folders. 

>:point_right: It is important to date folders so the latest would come at the top of the sorted list.

Here is an example of the repository structure:
```
├── dataset-1-0
│   ├── 20220202
│   │   ├── annotation
│   │   │   ├── dbpedia
│   │   │   ├── geonames
│   │   │   └── wikidata
│   │   ├── indexing
│   │   │   ├── en
│   │   │   └── fr
│   │   ├── json
│   │   │   ├── coalesced
│   │   │   ├── fulltext
│   │   │   └── metadata
│   │   ├── labels
│   │   ├── pdf
│   │   ├── rdf
│   │   ├── txt
│   │   └── xml
├── pdf_cache
│   └── unreadable
└── training
    ├── en
    │   ├── test
    │   └── train
    └── fr
        ├── test
        └── train
```

At this point the following output is generated:
- single metadata.tsv file
- <paper_id>.json containing titles, abstracts, detected languages according to the [schema](../../doc/ISSA_json_schema.txt) .
- <paper_id>.url files containing PDF URLs to be used to download actual PDF files.
- (optionally) <paper_id>.tsv files with descriptors' URIs and labels to be used for training indexing models
- (optionally) <paper_id>.txt files with text from metadata that can be used for training indexing models in case if PDF is not available




 