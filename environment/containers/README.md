# Docker containers

Almost all of the tools used in the ISSA pipeline are executed within a docker container context. That provides greater portability and maintainability of the execution environment.

### Configuration

Variable aspects of docker containers such as directories, languages, etc. are configured in [env.sh](../../env.sh) file.

### Execution

Each container folder typically contains: 
- docker image installation or build script
- docker container run script

All of the containers, except for `virtuoso`, are started and stopped as they are needed. The `virtuoso` container should be constantly running to provide access to the generated Knowledge Graph. 

>:point_right:  The `dbpedia-spotlight` English container requires a lot of memory and fails to execute on a 32Gb RAM machine if any other container besides `virtuoso` is running.

### Storage
Each docker container is provided with a persistent storage directory on the host machine through the mapped volumes mechanism. These volumes can store models, configurations and database files. The volumes are created in the `ISSA/volumes` directory.

If a docker container has to access pipeline-generated files or pipeline scripts their locations are mapped to the `issa/data` and `issa/scripts` directories in the containers.

## Containers

### annif

### agrovoc-pyclinrec

### dbpedia-spotlight

### entity-fishing

### grobid

### mongodb

### virtuoso

The virtuoso container provides storage for pipeline-generated Knowledge Graph and access to it via the SPARQL endpoint.

We deploy [OpenLink Virtuoso Enterprise Edition 7.2 Docker Image](https://hub.docker.com/r/openlink/virtuoso-closedsource-8) and configure it to be integrated into the pipeline. 

Before running the container for the first time it is necessary to create a dba password and store it in the VIRTUOSO-PWD env variable. (We choose to hide the variable in the user's `.bashrc` file. If you do the same remember to restart the user's session.)

- to install the image and configure Virtuoso run [install-virtuoso.sh](vistuoso/install-virtuoso.sh) script.

- to run the container invoke [run-virtuoso.sh](vistuoso/install-virtuoso.sh) script. 

- to access the SPARQL endpoint send HTTP request to `http://<host_name>:8890/sparql`.

>:point_right: This container should not be stopped except for maintenance reasons.





