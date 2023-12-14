#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Indexing ISSA documents with descriptors

# ISSA environment definitions 
. ../env.sh

echo "************************************************************************"
echo " Indexing documents with descriptors using Annif..."
echo "************************************************************************"


source ${ISSA_VENV}/bin/activate

pushd ./indexing

	python3 ./indexing_preprocess.py $ISSA_PIPELINE_CONFIG

	./run-annif-indexing.sh 

	python3 ./indexing_postprocess.py $ISSA_PIPELINE_CONFIG

popd

deactivate

