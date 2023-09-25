#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# 
# Run this script to restore the dataset in Virtuoso in case it was deleted or corrupted

# ISSA environment definitions
. ../../env.sh

echo "graph namespace  : $ISSA_NAMESPACE"
echo "input host rdf dir    : $VVIRTUOSO_HOST_DATA_DIR"
echo "import script dir: $VIRTUOSO_CONT_SCRIPT_DIR"

log_dir=$ISSA_PIPELINE_LOG
mkdir -p $log_dir
log=$log_dir/restore_virtuoso_$(date "+%Y%m%d_%H%M%S").log

# Start Virtuoso container if needed
CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME

# Clear all the graphs

docker exec -w $VIRTUOSO_CONT_SCRIPT_DIR $CONTAINER_NAME \
    	  isql -H localhost -U dba -P $VIRTUOSO_PWD \
       exec="LOAD ./delete-graphs.isql" \
                 -i $ISSA_NAMESPACE &>> $log


for directory in  $(ls -d $VIRTUOSO_HOST_DATA_DIR/$ISSA_DATASET/**/$REL_RDF/); do

	echo $directory

     container_directory=$(echo $directory | sed "s#$VIRTUOSO_HOST_DATA_DIR#$VIRTUOSO_CONT_DATA_DIR#g")

    echo $container_directory

	docker exec -w $VIRTUOSO_CONT_SCRIPT_DIR $CONTAINER_NAME \
    		  isql -H localhost -U dba -P $VIRTUOSO_PWD \
       	  exec="LOAD ./import.isql" \
                 -i $container_directory $ISSA_NAMESPACE &>> $log


done

