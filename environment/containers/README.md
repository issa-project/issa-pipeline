# Docker containers

All of the tools used in the ISSA pipeline are executed within a Docker container context. That provides greater portability and maintainability of the execution environment.

### Configuration

Variable aspects of Docker containers such as directories, languages, etc. are configured in env.sh files in [config](../../config) sub-directories.


### Execution

Each container folder typically contains:

- Docker image installation or build script `install-<contianer>.sh`
- Docker container run script `run-<contianer>.sh`

All of the containers, except for `virtuoso` and `sparql-micro-service`, are started and stopped as they are needed. The `virtuoso` and `sparql-micro-service` containers should be constantly running to provide access respectively to the generated Knowledge Graph and the SPARQL micro-services retrieving data from OpenAlex.

>:point_right:  The `dbpedia-spotlight.en` container requires a lot of memory and fails to execute on a 32Gb RAM machine if any other container besides `virtuoso` is running.

### Data persistence

Each Docker container is provided with a persistent storage directory on the host machine through the mapped volumes mechanism. These volumes can store models, configurations and database files. The volumes are created in the `/volumes` directory in the host FS.

If a Docker container has to access pipeline-generated files or pipeline scripts their locations are mapped to the `issa/data` and `issa/scripts` directories in the containers' FS.

## Containers

### annif

The `annif` container provides automated indexing of documents' text in the pipeline. For training the statistical models provided by Annif software we create a separate `annif-training` container (see [training](../../training) ) for more details. But both containers share the same project directory on the host FS.

We deploy [Annif Docker Image](https://github.com/NatLibFi/Annif/wiki/Usage-with-Docker) and configure the models that we would like to train and use on the document corpus. The [project config file](annif/projects.cfg) should be adapted for each use case.

- to install the image run [install-annif.sh](annif/install-annif.sh) script.
- to run the container invoke [run-annif.sh](annif/run-annif.sh) script.
- to test the installation and configuration run 
  - ```docker exec annif annif list-projects```
 
 >:point_right: The [training](../../training) process has to be run at least once before the automated indexing is feasible.

 More details about usage and configuration of `annif` container can be found [in the Annif documentation]](https://github.com/NatLibFi/Annif/wiki/Usage-with-Docker).

### dbpedia-spotlight
Two dbpeadia-spotlight containers are created from the [DBpedia Spotlight Docker image](https://hub.docker.com/r/dbpedia/dbpedia-spotlight) one per language `dbpedia-spotlight.en` and `dbpedia-spotlight.fr`. Each container relies on the downloaded language model. The model download is lengthy (on our machine 11 and 4 min for English and French) and is included in the installation script. The models are stored in the host FS.

- to install the image and download language models run [install-spotlight.sh](dbpedia-spotlight/install-spotlight.sh) script.

- to run the containers invoke [run-spotlight.sh](dbpedia-spotlight/run-spotlight.sh) script.
- to test annotation call
  - ```curl -X POST http://localhost:2222/rest/annotate --data-urlencode "text=Growing bananas in Ireland" --data-urlencode "lang=en" --data-urlencode "confidence=0.15" -H "Accept: application/json"``` 
  - ```curl -X POST http://localhost:2223/rest/annotate --data-urlencode "text=Cultiver des bananes en Irlande" --data-urlencode "lang=fr" --data-urlencode "confidence=0.15" -H "Accept: application/json"```

>:point_right:  The `dbpedia-spotlight.en` container requires a lot of memory and fails to execute on a 32Gb RAM machine if any other container besides `virtuoso` is running. It is also slow to launch and cannot be accessed immediately. We allocate a 2 min delay after the container start command.

>:point_right: To update the models it is sufficient to delete the model folder and re-run the container installation script.

Read the docs for the `dbpedia-spotlight` container: https://hub.docker.com/r/dbpedia/dbpedia-spotlight

### entity-fishing

The `entity-fishing` container is created from the original [entity-fishing docker image](https://nerd.readthedocs.io/en/latest/docker.html) and provides general entity recognition and disambiguation against Wikidata. Entity-fishing also requires the models to be downloaded during the installation.

- to install the image and download language models run [install-entity-fishing.sh](entity-fishing/install-entity-fishing.sh) script.
- to run the containers invoke [run-entity-fishing.sh](entity-fishing/run-entity-fishing.sh) script. 
- to test annotation call 
  - ```curl -X POST http://localhost:8090/service/disambiguate -X POST -F "query={ 'text':'Growing bananas in Ireland', 'language': {'lang':'en'}}" -H "Accept: application/json"``` 
  - ```curl -X POST http://localhost:8090/service/disambiguate -X POST -F "query={ 'text':'Cultiver des bananes en Irlande', 'language': {'lang':'fr'}}" -H "Accept: application/json"``` 

>:point_right: To update the models run [install-models.sh](entity-fishing/install-models.sh) script. 

### grobid

The `grobid` container provides text extraction from the PDF documents of the corpus articles.

We deploy the [CRF-only image](https://grobid.readthedocs.io/en/latest/Grobid-docker/) since our host machine does not have a GPU for CRF and Deep Learning image. No additional configuration is required.

- to install the image run [install-grobid.sh](grobid/install-grobid.sh) script.
- to run the containers invoke [run-grobid.sh](grobid/run-grobid.sh) script.
- to test run the command `curl http://localhost:8070/api/version`

### morph-xr2rml

Deployed during ISSA-2, the utilization of Morph-xR2RML docker container provides the seamless mapping of the JSON documents to the RDF dataset. In fact, the transformation is a two step process: the first step loads the set of JSON documents or a tab-delimited file to the MongoDB database and the second step maps the MongoDB database to the RDF triples.

The container network deployment is adapted from the [Morph-xR2RML](https://github.com/frmichel/morph-xr2rml/tree/master/docker) repository. The tool connects two Docker images [MongoDb Docker Image](https://hub.docker.com/_/mongo) and [morph-xr2rml](https://hub.docker.com/r/frmichel/morph-xr2rml) and contains the preloaded scripts to execute transformation.

- to install Morph-xR2RML run [install-morph-xr2rml-ISSA.sh](morph-xr2rml/install-morph-xr2rml-ISSA.sh) script.
- to run Morph-xR2RML run [run-morph-xr2rml-ISSA.sh](morph-xr2rml/run-morph-xr2rml-ISSA.sh) script.

>:point_right: TO run the Morph-xR2RML tool the Docker Compose hast to be installed. See [Docker Compose installation](https://docs.docker.com/compose/install/).

### pyclinrec

The `pyclinrec` container runs the text annotation service to annotate text with concepts from a custom dictionary such as [Agrovoc Multilingual Thesaurus](https://agrovoc.fao.org) or [MeSH](https://www.nlm.nih.gov/mesh/meshhome.html).

We build a Docker image to create the execution environment for the [Python Concept Recognition Library](https://github.com/twktheainur/pyclinrec) and access the functionality through a web application similar to other annotation Dockers, e.g. `dbpedia-spotlight` or `entity-fishing`.

- to build the image and initialize pyclinrec container invoke [install-pyclinrec.sh](pyclinrec/install-pyclinrec.sh) script.
- to run the container invoke [run-pyclinrec.sh](pyclinrec/run-pyclinrec.sh) script.
- to get help call `http://localhost:5002/`
- to test annotation call
  - ```curl -X POST http://localhost:5002/annotate --data-urlencode "text=Growing bananas in Ireland" --data-urlencode "lang=en" --data-urlencode "conf=0.15" -H "Accept: application/json"``` 
  - ```curl -X POST http://localhost:5002/annotate --data-urlencode "text=Cultiver des bananes en Irlande" --data-urlencode "lang=fr" --data-urlencode "conf=0.15" -H "Accept: application/json"```

>:point_right: The internal vocabulary and concept indexing is taking place during the first run of the Docker container and may take a long time. On our machine, the initialization takes about 10 minutes for Agrovoc dictionaries.

More details on the container configuration and usage can be found in the [pyclinrec](pyclinrec/README.md) folder.

### virtuoso

The `virtuoso` container provides storage for pipeline-generated Knowledge Graph and access to it via the SPARQL endpoint.

We deploy [OpenLink Virtuoso Enterprise Edition 7.2 Docker Image](https://hub.docker.com/r/openlink/virtuoso-closedsource-8) and configure it to be integrated into the pipeline. 

Before running the container for the first time it is necessary to create a dba password and store it in the $VIRTUOSO_PWD env variable. (We choose to set the variable in the user's `.bashrc` file. If you do the same remember to restart the user's session.)

- to install the image and configure Virtuoso run [install-virtuoso.sh](vistuoso/install-virtuoso.sh) script.
- to run the container invoke [run-virtuoso.sh](vistuoso/install-virtuoso.sh) script.
- to access the SPARQL endpoint send HTTP request to `http://<host_name>:8890/sparql`.

>:point_right: This container should not be stopped except for maintenance reasons.

>:point_right: Each instance of ISSA knowledge graph requires a separate Virtuoso container.

More details on the container configuration and usage can be found in the [virtuoso](virtuoso/README.md) folder.

### sparql-micro-service

[SPARQL micro-services](https://github.com/frmichel/sparql-micro-service) translate the result of Web APIs into an RDF representation.

In ISSA, they are used to invoke several services of the [OpenAlex API](https://docs.openalex.org/) to retrieve, for each article having a DOI, the follwing items:
- the ordered list of authors and affiliations with their ids (OpenAlexID and ORCID)
- the Sustainable Development Goals (SDG) that the article pertains to
- the OpenAlex topics/sub-fields/fields/domains
