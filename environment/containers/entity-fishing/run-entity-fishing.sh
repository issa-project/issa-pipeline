#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../../../env.sh

echo $EF_MODELS_DIR

# Run EF docker container 
CONTAINER_NAME=${EF_CONT_NAME:-entity-fishing}

if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
     echo "starting $CONTAINER_NAME container"

	docker run --name $CONTAINER_NAME \
                -d \
                -p 8090:8090 \
                -v $EF_MODELS_DIR:/opt/entity-fishing/data/db \
                entity-fishing			 
     
     echo "started $CONTAINER_NAME container"
     echo "waiting for models to load" 
	sleep 1m
fi

echo "$CONTAINER_NAME is running"

popd
