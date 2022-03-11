#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Generate training dataset from data in th e current ISSA dataset to train Annif models

# ISSA environment definitions 
. ../env.sh

source ${ISSA_VENV}/bin/activate

# Create dataset files
pushd ../pipeline/indexing

python3 ./training_dataset.py

popd


# Create vocabulary files
echo $(date "+%Y%m%d_%H%M%S")

pushd ../environment/datasets/agrovoc

python3 -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab('en', 'agrovoc-en.ttl')"
cp -v agrovoc-en.ttl $ANNIF_TRAINING_DIR/en

python3 -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab('fr', 'agrovoc-fr.ttl')"
cp -v agrovoc-fr.ttl $ANNIF_TRAINING_DIR/fr

popd

echo $(date "+%Y%m%d_%H%M%S")

deactivate

