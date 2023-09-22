#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load Agrovoc thesaurus into Virtuoso triplestore

# ISSA environment definitions
. ../../../env.sh

log_dir=$ISSA_ENV_LOG
mkdir -p $log_dir 
log=$log_dir/agrovoc_import_$(date "+%Y%m%d_%H%M%S").log


CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME

cp -v import-agrovoc.isql "$AGROVOC_IMPORT_DIR"                 >>$log

docker exec $CONTAINER_NAME \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD /database/import/import-agrovoc.isql"    &>>$log



