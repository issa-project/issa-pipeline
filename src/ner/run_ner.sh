#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA run Named Entities Recognition

# ISSA environment definitions & export
. ../env.sh

CURRENT_TIME=$(date "+%Y%m%d_%H%M%S")

source ${ISSA_VENV}/bin/activate

pushd ./cord19_ner/script

python3 ./main_threading.py

popd

deactivate



