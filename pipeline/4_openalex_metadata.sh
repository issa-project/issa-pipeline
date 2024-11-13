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

#activate the virtual environment
source ${ISSA_VENV}/bin/activate

pushd ./openalex

	echo "*********************************************************************" > $log
	echo "*** Retrieving metadata from OpenAlex..." >> $log
	python3 ./retrieve_openalex_data.py	$ISSA_PIPELINE_CONFIG 	--datatype authorships
	sleep 1
	python3 ./retrieve_openalex_data.py	$ISSA_PIPELINE_CONFIG 	--datatype sdgs
	sleep 1
	python3 ./retrieve_openalex_data.py	$ISSA_PIPELINE_CONFIG 	--datatype topics

	echo "*** Copying RDF files to $OPENALEX_IMPORT_DIR..." >> $log
	cp -v $LATEST_UPDATE_DIR/$REL_RDF/issa-document-openalex*.ttl $OPENALEX_IMPORT_DIR >> $log
	
popd

# deactivate the virtual environment
deactivate
