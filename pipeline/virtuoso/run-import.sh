#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../../env.sh

echo "input rdf dir: $VIRTUOSO_IMPORT_DIR"


# Start container if needed
docker start virtuoso

log_dir=../logs 
mkdir -p $log_dir
log=$log_dir/import_virtuoso_$(date "+%Y%m%d_%H%M%S").log

if [ $( docker ps -f name=virtuoso | wc -l ) -gt 1 ]; then 

	docker exec -w $VIRTUOSO_CONT_SCRIPT_DIR \
		  virtuoso isql -H localhost -U dba -P $VIRTUOSO_PWD exec="LOAD ./import-all.isql" -i $VIRTUOSO_IMPORT_DIR &>> $log

fi
