#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../env.sh

log_dir=./logs 
mkdir -p $log_dir
log_dir=$(readlink -f $log_dir)
log_file=$log_dir/annif-generate-vocabs_$(date "+%Y%m%d_%H%M%S").log

#activate the virtual environment
source ${ISSA_VENV}/bin/activate
echo "Generating vocabularies..."

pushd ../environment/datasets/agrovoc

python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab('en', 'agrovoc-en.ttl')"  &>>$log_file
#python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab_with_parent_labels('en', 'agrovoc-ext-en.ttl')"
#python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab_with_parent_labels_for_non_leaves('en', 'agrovoc-alt-en.ttl')"
mv -v agrovoc-en.ttl $ANNIF_TRAINING_DIR/en  &>>$log_file


python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab('fr', 'agrovoc-fr.ttl')"  &>>$log_file
#python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab_with_parent_labels('fr', 'agrovoc-ext-fr.ttl')"
#python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab_with_parent_labels_for_non_leaves('fr', 'agrovoc-alt-fr.ttl')"
mv -v agrovoc-fr.ttl $ANNIF_TRAINING_DIR/fr  &>>$log_file

popd

deactivate
