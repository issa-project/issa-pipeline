To transform pipeline collected data into [RDF](https://www.w3.org/RDF/)  using [Morph-xR2RML](https://github.com/frmichel/morph-xr2rml) tool the data has to be in presented to the tool in queryable storage. In ISSA we chose to use MongoDB as an intermediate queryable database storage as the most suitable for the JSON import.

This folder provides the scripts needed for loading and [aggregating data](https://www.mongodb.com/docs/manual/aggregation/) in MongoDB.

- [run_import.sh](./run_import.sh) - main entry point for data import. It maps the metadata file and JSON files to MongoDB collections and loads them into the database.
- [drop_database.sh](./drop_database.sh) - script to drop the database. Used if the MongoDB storage isconfigured as transient meaning that the data is deleted after the transformation to RDF is done
- [aggregate_descriptors.js](./aggregate_descriptors.js) - MongoDB script to save the thematic descriptors, document domains, and authors' keywords into separate collections to aid xR2RML transformation.
- _filter*.js_ - MongoDB scripts providing additional filtering of the verbose annotations, e.g. to remove the annotations with low confidence scores, beginning with digits, etc.

The scripts MongoDB scripts are called from [run_import.sh](./run_import.sh) as a part of the import.
