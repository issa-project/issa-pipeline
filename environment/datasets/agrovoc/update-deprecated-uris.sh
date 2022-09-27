#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load Agrovoc thesaurus into Virtuoso triplestore

# ISSA environment definitions
. ../../../env.sh

log_dir=../../logs
mkdir -p $log_dir 
log=$log_dir/agrovoc_update_deprecated_$(date "+%Y%m%d_%H%M%S").log

docker start virtuoso

cp -v update-deprecated-uris.isql "$AGROVOC_IMPORT_DIR"                 >>$log

docker exec virtuoso \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD /database/import/update-deprecated-uris.isql"    &>>$log



