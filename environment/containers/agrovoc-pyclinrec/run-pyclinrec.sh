#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# This script can be called by sumbolic links in the pipeline 
# so we need to make sure that the relative path still works
pushd $(dirname $(readlink -f "$0" ))

# ISSA environment definitions
. ../../../env.sh

# Run pyclinrec docker container 
CONTAINER_NAME=agrovoc-pyclinrec

# Make a dictionary on the host for persistent cache
mkdir -p $PYCLINREC_HOST_CACHE
chmod 666 $PYCLINREC_HOST_CACHE

if [ -z "$(ls $PYCLINREC_HOST_CACHE )" ]; then
   echo "Runinig container for the first time to initialize the dictionaries 
and recognizers.It may take a long time ( ~10 min).
Run command <docker logs $CONTAINER_NAME> to see if the initialization is complete."

fi


if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
     echo "starting $CONTAINER_NAME container"

	docker run --name $CONTAINER_NAME \
                -d \
                -p 5000:5000 \
                -v $PYCLINREC_HOST_CACHE:/app/cache \
                pyclinrec:0.10
     
     echo "started $CONTAINER_NAME container"
fi

echo "$CONTAINER_NAME is running"

popd

