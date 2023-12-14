#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../env.sh

# Run Annif docker container 
IMAGE=quay.io/natlibfi/annif:0.55 
CONTAINER_NAME=annif-training

if [ $( docker ps -f name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
     echo "starting annif container"
	docker run --name $CONTAINER_NAME \
                -itd --rm \
                -p 5001:80 \
                -v $ANNIF_PROJECTS_DIR:/annif-projects \
                -v $ANNIF_TRAINING_DIR:/training/data-sets \
			 -u $(id -u):$(id -g) \
                $IMAGE bash		 
     #sleep 2s
     echo "started $CONTAINER_NAME container"
fi

docker start $CONTAINER_NAME

echo "$CONTAINER_NAME container is running"

# Copy training scripts 
#cp -v ./projects.cfg $ANNIF_PROJECTS_DIR 
cp -v ./train-and-evaluate_en.sh $ANNIF_PROJECTS_DIR
cp -v ./train-and-evaluate_fr.sh $ANNIF_PROJECTS_DIR

# Run training and evaluation scripts

for lang in en fr; do

	log_dir=./logs 
	mkdir -p $log_dir
	log_file=$log_dir/annif-training_$lang_$(date "+%Y%m%d_%H%M%S").log

     docker exec -it $CONTAINER_NAME ./train-and-evaluate_$lang.sh &>>$log_file

done

docker stop $CONTAINER_NAME
