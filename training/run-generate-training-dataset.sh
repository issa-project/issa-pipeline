#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Generate training dataset from data in the current ISSA dataset to train Annif models

# ISSA environment definitions 
. ../env.sh

log_dir=./logs 
mkdir -p $log_dir
log_dir=$(readlink -f $log_dir)
log_file=$log_dir/annif-generate-dataset_$(date "+%Y%m%d_%H%M%S").log


# Activate the virtual environment
source ${ISSA_VENV}/bin/activate

# Create dataset files
echo "Generating training corpus..."

pushd ../pipeline/indexing

python3 ./training_dataset.py $ISSA_PIPELINE_CONFIG          &>>$log_file

popd

deactivate

