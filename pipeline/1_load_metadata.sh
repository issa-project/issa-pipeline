#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# 
# Create ISSA metadata

# ISSA environment definitions
. ../env.sh

echo "$ISSA_DATASET"
echo "$LATEST_UPDATE"


echo "************************************************************************"
echo " Loading and processing corpus metadata..."
echo "************************************************************************"

#activate the virtual environment
source ${ISSA_VENV}/bin/activate

pushd ./metadata

	echo "*********************************************************************" >> $log
	echo "Downloading metadata..."
	python3 ./download_corpus_metadata.py $ISSA_PIPELINE_CONFIG

	echo "*********************************************************************" >> $log
	echo "Processing metadata..."
	python3 ./process_corpus_metadata.py  $ISSA_PIPELINE_CONFIG	

	echo "*********************************************************************" >> $log
	echo "Creating the dataset repository..."
	python3 ./process_corpus_metadata.py  $ISSA_PIPELINE_CONFIG	
	python3 ./create_dataset_repository.py $ISSA_PIPELINE_CONFIG

popd

# deactivate the virtual environment
deactivate
