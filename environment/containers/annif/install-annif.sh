#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA transform collected data to RDF format

# ISSA environment definitions
. ../../../env.sh

echo "Pulling original Annif image..."
docker pull quay.io/natlibfi/annif:0.56

# We built a custom image of Annif Docker to calculate a missing  F1@10 metric
# If this metric is not needed set $ANNIF_IMAGE=original in the env.sh file

if [ $ANNIF_IMAGE == issa ] ; then # pull our forked version 
     echo "Building custom Annif image..." 
	git clone https://github.com/issa-project/Annif.git
	docker pull python:3.8-slim-bullseye
	docker build --rm -t issa/annif:0.55
fi

cp ./projects.cfg $ANNIF_PROJECTS_DIR







