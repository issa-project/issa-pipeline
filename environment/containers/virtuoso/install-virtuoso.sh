#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


# ISSA environment definitions
. ../../../env.sh

# Pull Docker image
docker pull openlink/virtuoso-opensource-7:7.2

# Run for the first time to create database files
./run-virtuoso.sh

# Create import folder
mkdir ./import
docker cp ./import virtuoso:/database/
rm -d import 

# Copy virtuoso.ini
docker cp ./virtuoso.ini virtuoso:/database/virtuoso.ini

# Restart container
docker restart virtuoso




