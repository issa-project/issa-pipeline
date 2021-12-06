#!/bin/bash
# Authors: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# Environment definitions
. ../env.sh

# Run MongoDB docker container if specified 
CONTAINER_NAME='virtuoso'


if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
    docker run --name $CONTAINER_NAME \
          --rm -d \
          -p 8890:8890 -p 1111:1111 \
          -e DBA_PASSWORD=pass \
          -e DEFAULT_GRAPH=$VIRTUOSO_DEFAULT_GRAPH \
          -v $VIRTUOSO_DATABASE_VOLUME_DIR:/database \
          openlink/virtuoso-opensource-7:latest
    
     echo "started virtuoso container"
fi

echo "virtuoso container is running"



