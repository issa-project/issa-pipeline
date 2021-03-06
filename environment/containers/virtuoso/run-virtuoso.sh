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
CONTAINER_NAME=virtuoso


if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
    docker run --name $CONTAINER_NAME \
          -d \
          -p 8890:8890 -p 1111:1111 \
          -e DBA_PASSWORD=$VIRTUOSO_PWD \
          -e DEFAULT_GRAPH=$VIRTUOSO_DEFAULT_GRAPH \
          -v $VIRTUOSO_DATABASE_DIR:/database \
          -v $VIRTUOSO_HOST_DATA_DIR:$VIRTUOSO_CONT_DATA_DIR \
          -v $VIRTUOSO_HOST_SCRIPT_DIR:$VIRTUOSO_CONT_SCRIPT_DIR \
         openlink/virtuoso-opensource-7:7.2

     echo "starting virtuoso container..."
     sleep 30s    
fi

echo "virtuoso container is running"

popd

