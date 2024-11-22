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
    docker-compose start >> $log 2>&1
    sleep 10s
popd

# Activate the virtual environment
source ${ISSA_VENV}/bin/activate

pushd ./openalex

    echo "*********************************************************************" >> $log
    echo "Retrieving metadata from OpenAlex..." >> $log
    python3 ./retrieve_article_data.py    $ISSA_PIPELINE_CONFIG     --datatype authorships >> $log 2>&1
    sleep 1
    python3 ./retrieve_article_data.py    $ISSA_PIPELINE_CONFIG     --datatype sdgs >> $log 2>&1
    sleep 1
    python3 ./retrieve_article_data.py    $ISSA_PIPELINE_CONFIG     --datatype topics >> $log 2>&1

    echo "*********************************************************************" >> $log
    echo "Computing the Rao Stirling index..." >> $log
    mkdir -p $DATASET_ROOT_PATH/$LATEST_UPDATE/$REL_OPENALEX        >> $log 2>&1
    python3 ./retrieve_citation_data.py   $ISSA_PIPELINE_CONFIG     >> $log 2>&1
    python3 ./compute_rao_stirling.py     $ISSA_PIPELINE_CONFIG     >> $log 2>&1
    mv -f rao_stirling.json $DATASET_ROOT_PATH/$LATEST_UPDATE/$REL_OPENALEX >> $log 2>&1

popd

# Deactivate the virtual environment
deactivate

pushd $SPARQL_MICRO_SERVICE_DOCKER_COMPOSE_DIR
    echo "Stoping SPARQL micro-service Docker network..." >> $log
    docker-compose stop >> $log 2>&1
popd
