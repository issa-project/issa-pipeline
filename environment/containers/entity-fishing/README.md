This folder provides the Dockerfile and scripts to build and run docker container for **entity-fishing** NER.

To build the container run:
<code>docker build -t entity-fishing --file Dockerfile -x test</code>

To download the model data run:
<code>install-models.sh</code>

To run the container run:
<code>docker run --name entity-fishing -d -p 8090:8090 -v ~/entity-fishing/models:/opt/entity-fishing/data/db entity-fishing</code>
and wait for about 1 min for data to be loaded

To start/stop the container run:
<code>docker start entity-fishing</code>
and wait for about 1 min for data to be loaded
<code>docker start entity-fishing</code>


