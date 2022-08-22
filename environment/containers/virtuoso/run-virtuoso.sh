#!/bin/bash
# Authors: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# This script can be called by sumbolic links in the pipeline 
# so we need to make sure that the relative path still works
pushd $(dirname $(readlink -f "$0" ))

# Environment definitions
. ../../../env.sh

# Run Virtuso docker container  
CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}

# Make folders to be used for ISSA data uploads
mkdir -p $VIRTUOSO_HOST_DATA_DIR
mkdir -p $VIRTUOSO_HOST_SCRIPT_DIR

if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
    docker run --name $CONTAINER_NAME \
          -d --restart always \
          -p 8890:8890 -p 1111:1111 -p 4443:4443 \
          -e DBA_PASSWORD=$VIRTUOSO_PWD \
          -e DEFAULT_GRAPH=$VIRTUOSO_DEFAULT_GRAPH \
          -v $VIRTUOSO_DATABASE_DIR:/database \
          -v $VIRTUOSO_HOST_DATA_DIR:$VIRTUOSO_CONT_DATA_DIR \
          -v $VIRTUOSO_HOST_SCRIPT_DIR:$VIRTUOSO_CONT_SCRIPT_DIR \
         openlink/virtuoso-opensource-7:7.2

     echo "starting $CONTAINER_NAME container..."
     sleep 30s    
fi

echo "$CONTAINER_NAME container is running"

popd

