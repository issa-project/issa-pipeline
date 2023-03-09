#!/bin/bash
# Authors: Anna BOBASHEVA, University Cote d'Azur, Inria
#          Andon Tchechmedjiev, EuroMov DHM, Université de Montpellier, IMT Mines Alès
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


# ISSA environment definitions
. ../../../env.sh


# To build the container run:
#docker build -t entity-fishing --file Dockerfile -x test

# Pull entity-fishing author's docker image
docker pull grobid/entity-fishing:0.0.6

# To download the model data run:
install-models.sh
