#!/bin/bash
# Authors: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# Environment definitions
. ../../../env.sh

# Run Virtuoso docker container  
CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
HOST_ISQL_PORT=${VIRTUOSO_HOST_ISQL_PORT:-1111}
HOST_HTTP_PORT=${VIRTUOSO_HOST_HTTP_PORT:-8890}
HOST_HTTPS_PORT=${VIRTUOSO_HOST_HTTPS_PORT:-4443}


# Make folders to be used for ISSA data uploads
mkdir -p $VIRTUOSO_HOST_DATA_DIR
mkdir -p $VIRTUOSO_HOST_SCRIPT_DIR

if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
    docker run --name $CONTAINER_NAME \
          -d --restart always \
          -p $HOST_HTTP_PORT:8890 \
          -p $HOST_ISQL_PORT:1111 \
          -p $HOST_HTTPS_PORT:4443 \
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


