#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Reference:
# https://hub.docker.com/r/openlink/virtuoso-closedsource-8

export INSTANCE=agritrop

# ISSA environment definitions
. ../../../env.sh

# Pull Docker image
docker pull openlink/virtuoso-opensource-7:7.2

CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
HOST_ISQL_PORT=${VIRTUOSO_HOST_ISQL_PORT:-1111}
HOST_HTTP_PORT=${VIRTUOSO_HOST_HTTP_PORT:-8890}


# Prompt  to create a dba password 
if [[ -z "${VIRTUOSO_PWD}" ]]; then
  echo "Please create a dba account password and store it in the environment variable VIRTUOSO_PWD. 
You can hide it in the account's .bashrc file. If you do so you have to restart the user's session after that."
  
   exit
fi


# Run container for the first time to create database files;
# persist them on the host machine;
# create read/write import folder for general import
mkdir -p $VIRTUOSO_DATABASE_DIR/import
chmod -R 775 $VIRTUOSO_DATABASE_DIR

docker run --name $CONTAINER_NAME \
          --rm -d \
          -p $HOST_HTTP_PORT:8890 \
          -p $HOST_ISQL_PORT:1111 \
		  -e DBA_PASSWORD=$VIRTUOSO_PWD \
          -v $VIRTUOSO_DATABASE_DIR:/database \
         openlink/virtuoso-opensource-7:7.2

# Copy virtuoso.ini with some ISSA specific settings
docker cp ./virtuoso.ini $CONTAINER_NAME:/database/virtuoso.ini

# Stop container
#sudo docker restart $CONTAINER_NAME
docker stop $CONTAINER_NAME

echo "Next run script ./run-virtuoso.sh"  




