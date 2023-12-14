#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Install the Morph-xR2RML tool that transforms collected data into RDF format.


# ISSA environment definitions
. ../../../env.sh

echo "mongo database dir: $MORPH_XR2RML_HOST_DATABASE_DIR" 
echo "mongo tools dir   : $MORPH_XR2RML_HOST_TOOLS_DIR" 
echo "issa data dir     : $MORPH_XR2RML_HOST_DATA_DIR"
echo "issa import script: $MORPH_XR2RML_HOST_SCRIPT_DIR"

# Make folders to be used for ISSA data uploads
mkdir -p -m 775 $MORPH_XR2RML_HOST_VOLUME
cp -R -u -p ./mongo_tools $MORPH_XR2RML_HOST_VOLUME 
cp -R -u -p ./xr2rml_config $MORPH_XR2RML_HOST_VOLUME

mkdir -p -m 775 $MORPH_XR2RML_HOST_VOLUME/xr2rml_output
mkdir -p -m 777 $MORPH_XR2RML_HOST_LOG_DIR
mkdir -p -m 777 $MORPH_XR2RML_HOST_DATA_DIR
mkdir -p -m 775 $MORPH_XR2RML_HOST_TEMPL_DIR

mkdir -p -m 775 $MORPH_XR2RML_HOST_VOLUME/mongo_db
mkdir -p -m 775 $MORPH_XR2RML_HOST_VOLUME/mongo_import
mkdir -p -m 775 $MORPH_XR2RML_HOST_SCRIPT_DIR

# Create docker-compose.yml 
envsubst < "docker-compose-template.yml" > "docker-compose.yml"

docker-compose up -d

docker-compose stop


