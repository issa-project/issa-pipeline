This folder provides scripts to install the original Docker image and run the Docker container for *entity-fishing* NER.

To pull the entity-fishing docker image and download the language models run:

<code>install-entity-fishing.sh</code>

To only download the language models data run:

<code>install-models.sh</code>

>:point_right: the knowledge base, English and French models v.0.0.6 would be downloaded. The total size is around 29 GB compressed, and 90 GB uncompressed.

To run the container run:

<code>run-entity-fishing.sh</code>.

To start/stop the container run:

<code>docker start entity-fishing</code> and wait for about 1 min for data to be loaded.

<code>docker stop entity-fishing</code>




