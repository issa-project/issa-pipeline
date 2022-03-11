#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA index documents with Annif tool
#
# NOTE: The docker has to be re-run every time because the mounted data source directory changes

# ISSA environment definitions
. ../../env.sh

# Run Annif docker container 
CONTAINER_NAME=annif

IMAGE=quay.io/natlibfi/annif:0.56 
if [ $ANNIF_IMAGE == issa ] ; then
    IMAGE=issa/annif:0.55
fi

if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
     echo "starting annif container"
	docker run --name $CONTAINER_NAME \
                -itd --rm \
                -p 5000:80 \
                -v $ANNIF_PROJECTS_DIR:/annif-projects \
                -v $ANNIF_SOURCE_DIR:/source \
			 -u $(id -u):$(id -g) \
                $IMAGE bash		 
     #sleep 2s
     echo "started $CONTAINER_NAME container"
fi

echo "$CONTAINER_NAME container is running"




for lang in en fr; do

	log_dir=../logs 
	mkdir -p $log_dir
	log_file=$log_dir/annif-indexing_"$lang"_$(date "+%Y%m%d_%H%M%S").log

	if [ $( docker ps -f name=annif | wc -l ) -gt 1 ]; then 
	    	docker exec annif annif index \
                         --suffix $ANNIF_SUFFIX \
    					  --force \
                         --limit $ANNIF_LIMIT \
                         --threshold $ANNIF_THRESHOLD \
                         $ANNIF_PROJECT-$lang \
    					 /source/$lang | tee $log_file
    fi

done 

docker stop annif
