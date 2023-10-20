#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load data into Virtuoso triple store 

# ISSA environment definitions
. ../env.sh

echo "************************************************************************"
echo " Uploading generated RDF (Turtle) files to triplestore..."
echo "************************************************************************"

pushd ./virtuoso

	./run-import.sh


echo "************************************************************************"
echo " Updating dataset metadata..."
echo "************************************************************************"

 	./import-dataset-meta.sh
	./update-dataset-meta.sh


popd