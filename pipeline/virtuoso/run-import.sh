#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../../env.sh

echo "graph namespace  : $ISSA_NAMESPACE"
echo "input rdf dir    : $VIRTUOSO_CONT_DATA_IMPORT_DIR"
echo "import script dir: $VIRTUOSO_CONT_SCRIPT_DIR"

log_dir=$ISSA_PIPELINE_LOG
mkdir -p $log_dir
log=$log_dir/import_virtuoso_$(date "+%Y%m%d_%H%M%S").log

# Start Virtuoso container if needed
CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME

docker exec -w $VIRTUOSO_CONT_SCRIPT_DIR $CONTAINER_NAME \
    isql -H localhost -U dba -P $VIRTUOSO_PWD \
        exec="LOAD ./import.isql" \
        -i $VIRTUOSO_CONT_DATA_IMPORT_DIR $ISSA_NAMESPACE &>> $log

