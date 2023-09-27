#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Install either Annif image from the docker hub or build a custom image 

# This script can be called by sumbolic links in the pipeline 
# so we need to make sure that the relative path still works
pushd $(dirname $(readlink -f "$0" ))

# ISSA environment definitions
. ../../../env.sh

# Run Annif docker container 
CONTAINER_NAME=annif
IMAGE=quay.io/natlibfi/annif:0.55 

if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
     echo "starting annif container"
	docker run --name $CONTAINER_NAME \
                -itd \
                -p 5000:80 \
                -v $ANNIF_PROJECTS_DIR:/annif-projects \
                -v $ANNIF_HOST_DATA_DIR:$ANNIF_CONT_DATA_DIR \
			 -u $(id -u):$(id -g) \
                $IMAGE bash		 
     #sleep 2s
     echo "started $CONTAINER_NAME container"
fi

echo "$CONTAINER_NAME container is running"

popd