#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#


# ISSA environment definitions
. ../../../env.sh

echo "Puling original Annif image..."
docker pull quay.io/natlibfi/annif:0.55

mkdir -p $ANNIF_PROJECTS_DIR
cp ./projects.cfg $ANNIF_PROJECTS_DIR







