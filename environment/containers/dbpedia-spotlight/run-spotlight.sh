#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# This script can be called by sumbolic links in the pipeline 
# so we need to make sure that the relative path still works
pushd $(dirname $(readlink -f "$0" ))

# ISSA environment definitions
. ../../../env.sh

# Run DBPedia-Spoltight docker containers, one per language

port=2222
wait=0

for lang in $SPOTLIGHT_LANGUAGES; do
 
    CONTAINER_NAME=dbpedia-spotlight.$lang 

	if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 

        echo "starting $CONTAINER_NAME container"
	   docker run --name $CONTAINER_NAME \
                -d \
                -p $port:80 \
                -v $SPOTLIGHT_MODELS_DIR:/opt/spotlight/models \
                dbpedia/dbpedia-spotlight spotlight.sh $lang
			 
        let port=port+1
        let wait=1 

        echo "started $CONTAINER_NAME container"
        echo "recommended wait time at least 2 min before executing a request to the Spotlight"
     fi

     echo "$CONTAINER_NAME container is running"

done

# Uncomment if the pause is needed
if [ $wait -eq 1 ]; then
   echo "waiting for models to load..."
   sleep 2m
fi

popd

