# ISSA dataset description

In this directory we provide the overall dataset metadata, schema definitions, and provenance entities definitions.  

Most of the triples are static and have to be defined and loaded once but the dates and triple counts can be updated after each update of the Knowlege Graph. The pipeline calls these *isql* scripts after each update of the Knowledge Graph.   

The scripts to [import](./import-dataset.sh) te dataset metadata and [update](./update-dataset.sh) triple counts are here as well. The dataset matadata is saved in the <http://data-issa.cirad.fr/graph/dataset> graph.  


>:point_right: The Turtle files and [update-dataset.isql](./update-dataset.isql) have to be adapted to each use case of ISSA.
