This folder provides the Dockerfile and scripts to build and run docker container for *entity-fishing* NER.

To build the container run:

<code>docker build -t entity-fishing --file Dockerfile -x test</code>

To download the models data run:

<code>wget https://science-miner.s3.amazonaws.com/entity-fishing/0.0.4/linux/db-kb.zip</code> and 

<code>wget https://science-miner.s3.amazonaws.com/entity-fishing/0.0.4/linux/db-$lang.zip</code> for each language.

To run the container run:

<code>docker run --name entity-fishing -d -p 8090:8090 -v ~/entity-fishing/models:/opt/entity-fishing/data/db entity-fishing</code>.

To start/stop the container run:

<code>docker start entity-fishing</code> and wait for about 1 min for data to be loaded.

<code>docker stop entity-fishing</code>

The *run-ef.sh* starts the *entity-fishing service* inside the container and should not be executed on the host. The *install-entity-fishong.sh*, *install-models.sh* and *run-entity-fishong.sh* are helper scripts to build, install and run the entity-fishing Docker container.  



