#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA create metadata

# ISSA environment definitions
. ../../env.sh

#activate virtual environment
source ${ISSA_VENV}/bin/activate

#python3 ./load_vocabulary.py --lang en --output agrovoc-en.ttl
python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab('en', 'agrovoc-en.ttl')"
#python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab_with_parent_labels('en', 'agrovoc-ext-en.ttl')"
#python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab_with_parent_labels_for_non_leaves('en', 'agrovoc-alt-en.ttl')"



#python3 ./load_vocabulary.py --lang fr --output agrovoc-fr.ttl
python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab('fr', 'agrovoc-fr.ttl')"
#python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab_with_parent_labels('fr', 'agrovoc-ext-fr.ttl')"
#python -c "from agrovoc_wrapper import Agrovoc_Wrapper; Agrovoc_Wrapper().download_vocab_with_parent_labels_for_non_leaves('fr', 'agrovoc-alt-fr.ttl')"

#deactivate virtual environment
deactivate
