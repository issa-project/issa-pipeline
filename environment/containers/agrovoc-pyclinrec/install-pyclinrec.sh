#!/bin/bash
# Authors: Anna BOBASHEVA, University Cote d'Azur, Inria
#          Andon Tchechmedjiev, EuroMov DHM, Université de Montpellier, IMT Mines Alès
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


# ISSA environment definitions
. ../../../env.sh


# To build the container run:
docker build --rm -f  Dockerfile -t pyclinrec:0.20 .

# Runinig the container for the first time to initialize the dictionaries and recognizers. 
# It may take a long time ( ~10 min). So it's better to do it now.

./run-pyclinrec.sh

echo "After checking if the initialization is complete run 
<docker stop> command to unload the container to free memory."