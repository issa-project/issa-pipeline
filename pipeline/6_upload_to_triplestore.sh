#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load data into Virtuoso triple store 

# ISSA environment definitions
. ../env.sh

pushd ./virtuoso

	./run-import.sh

popd

#update dataset metadata

pushd ../dataset
     
     ./import-dataset.sh
 	./update-dataset.sh

popd