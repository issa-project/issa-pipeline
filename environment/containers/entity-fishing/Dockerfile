## Docker entity-fishing image 
## adapted from Docker GROBID image and entity-fishing installation instructions
## adapted by Andon Tchechmedjiev for the ISSA project  

## See https://grobid.readthedocs.io/en/latest/Grobid-docker/
##     https://nerd.readthedocs.io/en/latest/build.html

## usage example 
## docker build -t entity-fishing --file Dockerfile -x test
## docker run --name entity-fishing --rm -d -p 8090:8090 -v ~/entity-fishing/models:/opt/entity-fishing/data/db entity-fishing
## where  ~/entity-fishing/models is a host file system directory for storing the entity-fishing models

# -------------------
# build builder image
# -------------------

#FROM openjdk:8u212-jdk as builder
FROM openjdk:8u275-jdk

USER root

RUN apt-get update && \
    apt-get -y --no-install-recommends install unzip git

WORKDIR /opt/

RUN git clone https://github.com/kermitt2/grobid.git  --branch 0.7.0
RUN cd grobid && ./gradlew clean install

RUN cd grobid/ && git clone https://github.com/kermitt2/grobid-ner.git && cd grobid-ner && \
        ./gradlew copyModels && ./gradlew clean install

WORKDIR /opt/
RUN git clone https://github.com/kermitt2/entity-fishing.git && cd entity-fishing && git checkout bd6db6d94ff7e5302085a2acb31e780d00b1552c && ./gradlew clean build -x test

COPY run-ef.sh /opt/

WORKDIR /opt/entity-fishing
CMD ["/opt/run-ef.sh"]
