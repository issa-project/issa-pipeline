#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../env.sh

#echo $ISSA_DATA_ROOT
#echo $ISSA_SRC_ROOT

# Directory where the output files are stored (relative to the current directory)
LOG_DIR=./logs 
mkdir -p $LOG_DIR

CURRENT_TIME=$(date "+%Y%m%d_%H%M%S")


# ------------------------------------------------------------------------------
# Run MongoDB docker container if specified 
CONTAINER_NAME='mongodb'

run_mongodb_container() {
    if [ "$MONGODB_CONTAINER" = true ] ; then
		if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
	    	#docker run --name mongodb_NAME -d --rm -p 27017:27017 -v ~/mongo:/data/db -v ~/data:/source -v ~/src:/scripts mongo:5.0.3
			docker run --name $CONTAINER_NAME -d --rm -p 27017:27017 -v ~/mongo:/data/db -v $ISSA_DATA_ROOT:/source -v $ISSA_SRC_ROOT:/scripts mongo:5.0.3
        fi
    fi
}

run_data_import() {
    if [ "$MONGODB_CONTAINER" = true ] ; then
		if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -gt 1 ]; then 
			docker exec mongodb ./scripts/mongo/import-issa.sh &>> $LOG_DIR/import-issa_${CURRENT_TIME}.log
 
        fi
    fi

}


run_mongodb_container
run_data_import