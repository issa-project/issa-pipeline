#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Grobid - pdf text extraction service

# This script can be called by a symbolic link from a different dir
# so we need to make sure that the relative path still works
pushd $(dirname $(readlink -f "$0" ))

# ISSA environment definitions 
. ../../../env.sh

CONTAINER_NAME=${GROBID_CONT_NAME:-grobid}

# Run Grobid docker container 

if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
     echo "starting $CONTAINER_NAME container"
     docker run --name $CONTAINER_NAME \
     -d \
	--init \
     -p 8070:8070 \
     -p 8071:8071 \
     lfoppiano/grobid:0.7.0			 

     echo "started $CONTAINER_NAME container"
fi

echo "$CONTAINER_NAME container is running"

popd 

