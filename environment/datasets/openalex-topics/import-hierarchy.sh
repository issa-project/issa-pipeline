#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Load OpenAlex topics labels and hierarchy into Virtuoso triplestore
#
# Parameters:
#   $1: file name of the OpenAlex topics hierarchy


# ISSA environment definitions
. ../../../env.sh

openalex_dump=$1


log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/openalex-topics-import-$(date "+%Y%m%d_%H%M%S").log

# Start container if needed
CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME

# Remove previously imported ttl files
rm -f -v $OPENALEX_IMPORT_DIR/$openalex_dump    >>$log

cp -v $openalex_dump        $OPENALEX_IMPORT_DIR          >>$log
cp -v import-hierarchy.isql $OPENALEX_IMPORT_DIR          >>$log

docker exec -w /database/import $CONTAINER_NAME \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD import-hierarchy.isql" -i $ISSA_NAMESPACE &>>$log
