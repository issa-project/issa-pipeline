#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA index text by Annif

# ISSA environment definitions 
. ../../../env.sh

# Run Grobid docker container 

if [ $( docker ps -f name=grobid | wc -l ) -eq 1 ]; then 
     echo "starting grobid container"
     docker run --name grobid \
     -d --rm \
	--init \ 
     -p 8070:8070 \
     -p 8071:8071 \
     lfoppiano/grobid:0.7.0			 

     echo "started grobid container"
fi

echo "grobid container is running"
