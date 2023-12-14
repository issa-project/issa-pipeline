#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load Agrovoc thesaurus into Virtuoso triplestore

# ISSA environment definitions
. ../../../env.sh

log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/import_mesh_$(date "+%Y%m%d_%H%M%S").log

VIRTUOSO=${VIRTUOSO_CONT_NAME:-virtuoso}

docker start $VIRTUOSO

cp -v import-mesh.isql "$MESH_IMPORT_DIR"                      >>$log

docker exec $VIRTUOSO \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD /database/import/import-mesh.isql"      &>>$log



