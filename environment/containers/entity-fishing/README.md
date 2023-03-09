This folder provides scripts to install original docker image and run docker container for *entity-fishing* NER.

To pull the entity-foshing docker image run:

<code>install-entity-fishing.sh</code>

To download the language models data run:

<code>install-models.sh</code>

>:point_right: the  knowlege base, English and French models are downloaded. Total size is around 29 GB compressed, and 90 GB uncompressed.

To run the container run:

<code>run-entity-fishing.sh</code>.

To start/stop the container run:

<code>docker start entity-fishing</code> and wait for about 1 min for data to be loaded.

<code>docker stop entity-fishing</code>




