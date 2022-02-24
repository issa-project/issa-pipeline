#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA create virtual environmet

# ISSA environment definitions
. ../../env.sh

python3 -m venv ${ISSA_VENV}

source ${ISSA_VENV}/bin/activate
pip install --upgrade pip

pip install -r requirements.txt

deactivate