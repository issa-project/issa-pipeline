#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# This script can be called by sumbolic links in the pipeline 
# so we need to make sure that the relative path still works
pushd $(dirname $(readlink -f "$0" ))

# ISSA environment definitions
. ../../../env.sh

# Run MongoDB docker container 
CONTAINER_NAME='mongodb'

if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
     echo "starting $CONTAINER_NAME container"
	docker run --name $CONTAINER_NAME \
                -d --rm \
                -p 27017:27017 \
                -v $MONGODB_DATABASE_DIR:/data/db \
                -v $MONGODB_SOURCE_DIR:/source \
                -v $MONGODB_IMPORT_DIR:/import \
                mongo:5.0.3
			 
     sleep 2s
     echo "started $CONTAINER_NAME container"
fi

echo "$CONTAINER_NAME container is running"

popd