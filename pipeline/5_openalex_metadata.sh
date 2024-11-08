#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# 
# ISSA environment definitions
. ../env.sh

echo "$ISSA_DATASET"
echo "$LATEST_UPDATE"


echo "************************************************************************"
echo " Retrieving additional metadata from OpenAlex..."
echo "************************************************************************"

#activate the virtual environment
source ${ISSA_VENV}/bin/activate

pushd ./openalex

	python3 ./retrieve_openalex_authorship.py	$ISSA_PIPELINE_CONFIG

popd

# deactivate the virtual environment
deactivate
