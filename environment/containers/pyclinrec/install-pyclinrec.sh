#!/bin/bash
# Authors: Anna BOBASHEVA, University Cote d'Azur, Inria
#          Andon Tchechmedjiev, EuroMov DHM, Université de Montpellier, IMT Mines Alès
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


# ISSA environment definitions
. ../../../env.sh


# To build the container run:
docker build --rm -f  Dockerfile -t pyclinrec:0.20 .

