#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA transform collected data to RDF format

# ISSA environment definitions
. ../env.sh

echo "************************************************************************"
echo "Start Morph_xR2RML Docker network..."
echo "************************************************************************"

pushd $MORPH_XR2RML_DOCKER_COMPOSE_DIR

	envsubst < "docker-compose-template.yml" > "docker-compose.yml"
	docker-compose start
    sleep 5s

popd

echo "************************************************************************"
echo "Import all data (meta, json ) to MongoDB..."
echo "************************************************************************"

# import all data (meta, json ) to the MongoDB
pushd ./morph-xr2rml/mongo

	./run-import.sh

popd

echo "************************************************************************"
echo "Transform from MongoDB to RDF (Turtle)..."
echo "************************************************************************"

pushd ./morph-xr2rml/xR2RML 

	./run-transformation.sh

popd

if ${ISSA_MONGODB_TRANSIENT:-false} ; then
echo "************************************************************************"
echo " Drop created MongoDB database after it was transformed ..."
echo "************************************************************************"

pushd ./morph-xr2rml/mongo

	./drop-database.sh

popd

fi

echo "************************************************************************"
echo "Stop Morph_xR2RML Docker network..."
echo "************************************************************************"

pushd $MORPH_XR2RML_DOCKER_COMPOSE_DIR

	docker-compose stop

popd
