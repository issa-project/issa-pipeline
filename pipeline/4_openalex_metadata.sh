#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# 
# ISSA environment definitions
. ../env.sh

echo "$ISSA_DATASET"
echo "$LATEST_UPDATE"

log_dir=$ISSA_PIPELINE_LOG
mkdir -p $log_dir 
log=$log_dir/retrieve-openalex-data-main-script-$(date "+%Y%m%d_%H%M%S").log
echo "" > $log

# Check if the Docker containers are running
echo "Starting SPARQL micro-service Docker network..." >> $log
pushd $SPARQL_MICRO_SERVICE_DOCKER_COMPOSE_DIR
	docker-compose start 2>&1 >> $log
	sleep 10s
popd

# Activate the virtual environment
source ${ISSA_VENV}/bin/activate

pushd ./openalex

	echo "*********************************************************************" >> $log
	echo "*** Retrieving metadata from OpenAlex..." >> $log
	python3 ./retrieve_openalex_data.py	$ISSA_PIPELINE_CONFIG 	--datatype authorships 2>&1 >> $log
	sleep 1
	python3 ./retrieve_openalex_data.py	$ISSA_PIPELINE_CONFIG 	--datatype sdgs 2>&1 >> $log
	sleep 1
	python3 ./retrieve_openalex_data.py	$ISSA_PIPELINE_CONFIG 	--datatype topics 2>&1 >> $log

	echo "*********************************************************************" >> $log
	echo "Copying RDF files to $OPENALEX_IMPORT_DIR..." >> $log
	cp -v $LATEST_UPDATE_DIR/$REL_RDF/issa-document-openalex*.ttl $OPENALEX_IMPORT_DIR 2>&1 >> $log
	
popd

# Deactivate the virtual environment
deactivate

pushd $SPARQL_MICRO_SERVICE_DOCKER_COMPOSE_DIR
	echo "Stoping SPARQL micro-service Docker network..." >> $log
	docker-compose stop 2>&1 >> $log
popd
