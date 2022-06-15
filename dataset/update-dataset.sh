#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load GeoNmaes graph into Virtuoso triplestore

# ISSA environment definitions
. ../env.sh

ISSA_VERSION=$ISSA_VERSION.$LATEST_UPDATE

log_dir=./logs
mkdir -p $log_dir 
log=$log_dir/dataset_meta_update_$(date "+%Y%m%d_%H%M%S").log

docker start virtuoso

cp -v update-dataset.isql "$DATASET_META_IMPORT_DIR"            #>>$log

docker exec virtuoso \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD /database/import/update-dataset.isql" -i $ISSA_VERSION  #&>>$log

echo "done."       