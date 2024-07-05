#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Load OpenAlex annotations into Virtuoso triplestore
#
# Parameters:
#   $1: file name of the annotations
#   $2: name of the ISQL import scrit


# ISSA environment definitions
. ../../../env.sh

dump=$1
isql_script=$2


log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/import-sdgs-metadata-$(date "+%Y%m%d_%H%M%S").log

# Start container if needed
CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME

# Remove previously imported ttl files
rm -f -v $OPENALEX_IMPORT_DIR/$dump                 >>$log

cp -v $dump             $OPENALEX_IMPORT_DIR        >>$log
cp -v $isql_script      $OPENALEX_IMPORT_DIR        >>$log

docker exec -w /database/import $CONTAINER_NAME \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD $isql_script" -i $ISSA_NAMESPACE &>>$log
