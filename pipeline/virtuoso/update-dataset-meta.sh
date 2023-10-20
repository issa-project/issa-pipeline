#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Update dataset metadata such as the number of triples and dates

# ISSA environment definitions
. ../../env.sh

ISSA_VERSION=$ISSA_VERSION.$LATEST_UPDATE

log_dir=$ISSA_PIPELINE_LOG
mkdir -p $log_dir 
log=$log_dir/update_dataset_meta_$(date "+%Y%m%d_%H%M%S").log

CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME

docker exec -w $VIRTUOSO_CONT_SCRIPT_DIR $CONTAINER_NAME \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD ./update-dataset-meta.isql" -i $ISSA_DATASET_NAME $ISSA_NAMESPACE $ISSA_VERSION  &>>$log

