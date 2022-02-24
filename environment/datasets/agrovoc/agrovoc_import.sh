#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA create metadata

# ISSA environment definitions
. ../../env.sh

./run-virtuoso

log_dir=../logs
mkdir -p $log_dir 
current_time=$(date "+%Y%m%d_%H%M%S")
log_file=$log_dir/agrovoc_import_${current_time}.log

cp -v import-agrovoc.isql "$AGROVOC_IMPORT_DIR" >>"$log_file"

# At the moment the dba/password are provided explicitly.
# In the future: hide
docker exec virtuoso \
            isql -H localhost -U dba -P pass \
            exec="LOAD /database/import/import-agrovoc.isql" &>>"$log_file"

