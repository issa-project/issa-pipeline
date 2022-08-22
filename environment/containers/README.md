# Docker containers

Almost all of the tools used in the ISSA pipeline are executed within a Docker container context. That provides greater portability and maintainability of the execution environment.

### Configuration

Variable aspects of Docker containers such as directories, languages, etc. are configured in [env.sh](../../env.sh) file.

### Execution

Each container folder typically contains: 
- Docker image installation or build script `install-<contianer>.sh`
- Docker container run script `run-<contianer>.sh`

All of the containers, except for `virtuoso`, are started and stopped as they are needed. The `virtuoso` container should be constantly running to provide access to the generated Knowledge Graph. 

>:point_right:  The `dbpedia-spotlight.en` container requires a lot of memory and fails to execute on a 32Gb RAM machine if any other container besides `virtuoso` is running.

### Storage
Each Docker container is provided with a persistent storage directory on the host machine through the mapped volumes mechanism. These volumes can store models, configurations and database files. The volumes are created in the `ISSA/volumes` directory.

If a Docker container has to access pipeline-generated files or pipeline scripts their locations are mapped to the `issa/data` and `issa/scripts` directories in the containers.

## Containers

### annif

### agrovoc-pyclinrec
The `agrovoc-pyclinrec` container runs the text annotation service to annotate text in English or French with concepts from the [Agrovoc Multilingual Thesaurus](https://agrovoc.fao.org).

We build a Docker image to create the execution environment for the [Python Concept Recognition Library](https://github.com/twktheainur/pyclinrec) and to create a web application similar to other annotation Dockers, e.g. `dbpedia-spotlight` and `entity-fishing`. NOTE: we forked the library for consistensy reasons). 

By default this container is created specifically for Agrovoc vocabulary but it can be reconfigured for another SKOS thesaurus by providing its SPARQL endpoint in `DICT_ENDPOINT` environment variable. If graph name filtering is required than a graph name can be passed in 'DICT_GRAPH' variable of the `docker run` command.

>:point_right: Concept recognition is currently available only for English and French.

- to build the image and initialise pyclinrec container invoke [install-pyclinrec.sh](agrovoc-pyclinrec/install-pyclinrec.sh) script.

- to run the container invoke [run-pyclinrec.sh](agrovoc-pyclinrec/run-pyclinrec.sh) script. 

- to get help call ```http://localhost:5000/```

- to test annotation call 

  - ```curl -X POST http://localhost:5000/annotate --data-urlencode "text=Growing bananas in Ireland" --data-urlencode "lang=en" --data-urlencode "conf=0.15" -H "Accept: application/json"``` 
  - ```curl -X POST http://localhost:5000/annotate --data-urlencode "text=Cultiver des bananes en Irlande" --data-urlencode "lang=fr" --data-urlencode "conf=0.15" -H "Accept: application/json"```

>:point_right: The internal vocabulary and concept indexing is taking place during the installation and it may take a long time. On our machinne the initialization takes about 10 minutes. 

### dbpedia-spotlight

### entity-fishing

### grobid

### mongodb

### virtuoso
The `virtuoso` container provides storage for pipeline-generated Knowledge Graph and access to it via the SPARQL endpoint.

We deploy [OpenLink Virtuoso Enterprise Edition 7.2 Docker Image](https://hub.docker.com/r/openlink/virtuoso-closedsource-8) and configure it to be integrated into the pipeline. 

Before running the container for the first time it is necessary to create a dba password and store it in the $VIRTUOSO-PWD env variable. (We choose to set the variable in the user's `.bashrc` file. If you do the same remember to restart the user's session.)

- to install the image and configure Virtuoso run [install-virtuoso.sh](vistuoso/install-virtuoso.sh) script.

- to run the container invoke [run-virtuoso.sh](vistuoso/install-virtuoso.sh) script. 

- to access the SPARQL endpoint send HTTP request to `http://<host_name>:8890/sparql`.

>:point_right: This container should not be stopped except for maintenance reasons.




