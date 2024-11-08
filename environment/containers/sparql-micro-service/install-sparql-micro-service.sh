#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Install the SPARQL micro-service containers on the host machine

# ISSA environment definitions
. ../../../env.sh

echo "services dir: $SPARQL_MICRO_SERVICE_HOST_SERVICES_DIR" 
mkdir -p -m 777 $SPARQL_MICRO_SERVICE_HOST_LOG_DIR
mkdir -p -m 775 $SPARQL_MICRO_SERVICE_HOST_SERVICES_DIR

# Create docker-compose.yml 
envsubst < "docker-compose-template.yml" > "docker-compose.yml"

docker-compose up -d

docker-compose stop
