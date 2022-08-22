#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA transform collected data to RDF format

# ISSA environment definitions
. ../env.sh


echo "************************************************************************"
echo "Import all data (meta, json ) to MongoDB..."
echo "************************************************************************"

docker start mongodb
sleep 5s

# import all data (meta, json ) to the MongoDB
pushd ./mongo

	./run-import.sh

popd

echo "************************************************************************"
echo "Transform from MongoDB to RDF (Turtle)..."
echo "************************************************************************"

pushd ./xR2RML 

	./run-transformation.sh

popd

docker stop mongodb