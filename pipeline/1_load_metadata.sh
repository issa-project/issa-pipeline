#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA create metadata

# ISSA environment definitions
. ../env.sh

#mkdir -p $ISSA_DATA_ROOT/$ISSA_DATASET

#activate virtual environment
source ${ISSA_VENV}/bin/activate

pushd ./metadata

	python3 ./download_agritrop_metadata.py
	python3 ./process_agritrop_metadata.py
	python3 ./create_dataset_repository.py

popd

#deactivate virtual environment
deactivate





