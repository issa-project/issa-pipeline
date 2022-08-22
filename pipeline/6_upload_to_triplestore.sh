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

	./import-all.sh

popd

echo "************************************************************************"
echo " Updating dataset metadata..."
echo "************************************************************************"

pushd ../dataset
     
     ./import-dataset.sh
 	./update-dataset.sh

     cp *.ttl $XR2RML_OUTPUT_DIR

popd