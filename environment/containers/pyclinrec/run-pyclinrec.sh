#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

export ISSA_INSTANCE=agritrop

# ISSA environment definitions
. ../../../env.sh

echo $PYCLINREC_HOST_CACHE
echo $PYCLINREC_DICT_ENDPOINT

# Run pyclinrec docker container 
CONTAINER_NAME=${PYCLINREC_CONT_NAME:-pyclinrec}

# Make a dictionary on the host for persistent cache
mkdir -p $PYCLINREC_HOST_CACHE
chmod 755 $PYCLINREC_HOST_CACHE

if [ -z "$(ls $PYCLINREC_HOST_CACHE )" ]; then
   echo "Runinig container for the first time to initialize the dictionaries 
and recognizers. It may take a long time ( ~10 min).
Run command <docker logs $CONTAINER_NAME> to see if the initialization is complete."

fi


if [ $( docker ps -af name=^/$CONTAINER_NAME$ | wc -l ) -eq 1 ]; then 
     echo "starting $CONTAINER_NAME container"

	docker run --name $CONTAINER_NAME \
                -itd \
                -p 5002:5000 \
			  -u $(id -u):$(id -g) \
                -v $PYCLINREC_HOST_CACHE:/app/cache \
                pyclinrec:0.20
     
	 sleep 5s
     echo "running $CONTAINER_NAME container"
else
     docker start $CONTAINER_NAME
     sleep 5s
fi

echo "Loading $PYCLINREC_DICT_NAME en dictionary"

SKOS_XL=${PYCLINREC_SKOS_XL_LABELS:-False}

curl -X POST http://localhost:5002/add_annotator \
--data-urlencode "name=$PYCLINREC_DICT_NAME" \
--data-urlencode "lang=en" \
--data-urlencode "endpoint=$PYCLINREC_DICT_ENDPOINT" \
--data-urlencode "graph=$PYCLINREC_DICT_GRAPH" \
--data-urlencode "skosXL=$SKOS_XL" \
-H "Accept: application/json"
echo

echo "Loading $PYCLINREC_DICT_NAME fr dictionary"
curl -X POST http://localhost:5002/add_annotator \
--data-urlencode "name=$PYCLINREC_DICT_NAME" \
--data-urlencode "lang=fr" \
--data-urlencode "endpoint=$PYCLINREC_DICT_ENDPOINT" \
--data-urlencode "graph=$PYCLINREC_DICT_GRAPH" \
--data-urlencode "skosXL=$SKOS_XL" \
-H "Accept: application/json"
echo



