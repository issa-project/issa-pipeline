#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA create metadata

# ISSA environment definitions
. ../env.sh

echo "$ISSA_DATASET"
echo "$LATEST_UPDATE"

echo "************************************************************************"
echo " Loading and processing corpus metadata..."
echo "************************************************************************"

#activate virtual environment
source ${ISSA_VENV}/bin/activate

pushd ./metadata

	python3 ./download_corpus_metadata.py
	python3 ./process_corpus_metadata.py
	python3 ./create_dataset_repository.py

popd

# deactivate virtual environment
deactivate





