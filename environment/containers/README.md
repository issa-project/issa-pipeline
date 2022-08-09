# Docker containers

Almost all of the tools use in ISSA are executed in the docker container context. This provides greater portability and maintainability of the execution enviromnet.

## General information

Many of the variable aspects of docker containers are configured in [env.sh](../../env.sh) file.

__Execution__
Each container folder contains: 
- docker image installation scripts
- docker container run scripts

All of the containers except for `virtuoso` are started and stopped as they are needed. The `virtuoso` container should be constantly runing providing the access to the build Knowledge Graph. 

>:point_right:  The `dbpedia-spotlight` English container requires a lot of memory and fails to execute on 32Gb RAM machine if any other container besides `virtuoso` is runing.

__Storage__
Each docker container is provided with a persistent storage directory on the host machine through the mapped volumes mechainism. These volumes can store models, configurations, database files. The volumes are created in `ISSA/volumes` directory.

If a docker container has to access pipeline generated files or pipeline scripts their locations are mapped to `issa/data` and `issa/scripts` directories in the containers.

## annif

## agrovoc-pyclinrec

## dbpedia-spotlight

## entity-fishing

## grobid

## mongodb

## virtuoso

Virtuoso container provides the storage for pipeline generated Knowlege Graph and the access to it throught the SPARQL endpoint.

We deploy [OpenLink Virtuoso Enterprise Edition 7.2 Docker Image](https://hub.docker.com/r/openlink/virtuoso-closedsource-8) and configure it to be integrated in the pipeline. 

Before runing the container for the first time it is nesessary to create a dba password and store it in the VIRTUOSO-PWD env variable. (We choose to hide the variable in the user's `.bashrc` file. If you do the same remember to restart the user's session.)

To install the image and configure Virtuoso run [install-virtuoso.sh](vistuoso/install-virtuoso.sh) script.

To run the container invoke [run-virtuoso.sh](vistuoso/install-virtuoso.sh) script

>:point_right: This container should not be stopped besides for maintenance reasons.

@Franck: instructions on how to access the sparql endpoint from the outside 




