#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../../../env.sh

echo $PYCLINREC_HOST_CACHE

# Run pyclinrec docker container 
CONTAINER_NAME=${PYCLINREC_CONT_NAME:-agrovoc-pyclinrec}

# Make a dictionary on the host for persistent cache
mkdir -p $PYCLINREC_HOST_CACHE
chmod 755 $PYCLINREC_HOST_CACHE

if [ -z "$(ls $PYCLINREC_HOST_CACHE )" ]; then
   echo "Runinig container for the first time to initialize the dictionaries 
and recognizers. It may take a long time ( ~10 min).
Run command <docker logs $CONTAINER_NAME> to see if the initialization is complete."

fi


if [ $( docker ps -af name=$CONTAINER_NAME | wc -l ) -eq 1 ]; then 
     echo "starting $CONTAINER_NAME container"

	docker run --name $CONTAINER_NAME \
                -itd \
                -p 5000:5000 \
			  -u $(id -u):$(id -g) \
                -v $PYCLINREC_HOST_CACHE:/app/cache \
                pyclinrec:0.20
     
     echo "running $CONTAINER_NAME container"
else
     docker start $CONTAINER_NAME
fi

if [ $(ls $PYCLINREC_HOST_CACHE | wc -l) -lt 4 ]; then
	echo "$CONTAINER_NAME is initializing..."
else
	echo "$CONTAINER_NAME is running"
fi

popd


