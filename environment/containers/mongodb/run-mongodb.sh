#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# This script can be called by a symbolic link from a differen tdir 
# so we need to make sure that the relative path still works
pushd $(dirname $(readlink -f "$0" ))

# ISSA environment definitions
. ../../../env.sh

echo "mongo database dir: $MONGODB_HOST_DATABASE_DIR" 
echo "issa data dir     : $MONGODB_HOST_DATA_DIR"
echo "issa import script: $MONGODB_HOST_SCRIPT_DIR"

# Make folders to be used for ISSA data uploads
mkdir -p $MONGODB_HOST_DATA_DIR
mkdir -p $MONGODB_HOST_SCRIPT_DIR
mkdir -p $MONGODB_HOST_DATABASE_DIR


# Run MongoDB docker container 
CONTAINER_NAME=${MONGODB_CONT_NAME:-mongodb}

if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
     echo "starting $CONTAINER_NAME container"
	docker run --name $CONTAINER_NAME \
                -d \
                -p $MONGODB_HOST_PORT:27017 \
                -v $MONGODB_HOST_DATABASE_DIR:/data/db \
                -v $MONGODB_HOST_DATA_DIR:$MONGODB_CONT_DATA_DIR \
                -v $MONGODB_HOST_SCRIPT_DIR:$MONGODB_CONT_SCRIPT_DIR \
                mongo:5.0.3
			 
     sleep 2s
     echo "started $CONTAINER_NAME container"
fi

echo "$CONTAINER_NAME container is running"

popd