This folder provides tools to import document corpus's metadata, text, and collected thematic descriptors and named entities (NE) annotations into MongoDB which is actually an intermediate step in data transformation of the RDF format by [xR2RML](../xR2RML) tool.

Bash scripts are used for import:
- `run-import.sh` is an  entry point  
- `import-tsv-file.sh` facilitates import from a single TSV file  
- `import-json-dir.sh` facilitates import from a directory containing one per document JSON files. 
- `import-tools.sh` defines helper functions to load groups of JSON files into MongoDB that are called by scripts above.

JavaScript scripts are used to manipulate on collections in MongoDB:
- `aggregate_descriptors.js` - creates a separate one-to-many collection for thematic descriptors from the "flattened" columns of `document_metadata` collection
- `filter_spotlight.js`     - (optionally) filter the Dbpedia NEs. The example script removes unnecessary fields from the spotlight collection as well as NEs that are less than 3 characters long or with similarity score lower than 0.75. 
- `filter_entityfishing.js`     - (optionally) filter the Wikidata NEs. The example script removes unnecessary fields from the entityfishing collection as well as NEs that are less than 3 characters long or having no associated *wikidataId*. 

>:point_right:  The `import-` scripts are executed in the context of [*MongoDB docker container*](../../environment/containers/mongodb) 

As a result, for each update of ISSA dataset a new database is created, e.g. `dataset-1-0-20220202` with following collections:  
- `document_metadata`    - loaded from the processed metadata TSV file
- `document_descriptors` - thematic descriptors extracted from the metadata by [aggregate_descriptors.js](aggregate_descriptors.js) script
- `article_text`         - text extracted for the open source articles loaded from a collection of JSON files
- `annif_descriptors`    - thematic descriptors identified by Annif loaded from a collection of JSON files
- `entityfishing`        - Wikidata NE annotations identified by entity-fishing service loaded from a collection of JSON files
- `geonames`             - Geonames NE annotations identified  by GeoNames recognizer routine loaded from a collection of JSON files
- `spotlight`            - DBPedia NE annotations identified by DBpedia Spotlight service loaded from a collection of JSON files

>:point_right: The locations of the input files are configured in [env.sh](../../env.sh)





