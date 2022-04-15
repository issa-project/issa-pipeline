#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Grobid - pdf text extraction service

# This script can be called by sumbolic links in the pipeline 
# so we need to make sure that the relative path still works
pushd $(dirname $(readlink -f "$0" ))


# ISSA environment definitions 
. ../../../env.sh

# Run Grobid docker container 

if [ $( docker ps -f name=grobid | wc -l ) -eq 1 ]; then 
     echo "starting grobid container"
     docker run --name grobid \
     -d \
	--init \
     -p 8070:8070 \
     -p 8071:8071 \
     lfoppiano/grobid:0.7.0			 

     echo "started grobid container"
fi

echo "grobid container is running"
