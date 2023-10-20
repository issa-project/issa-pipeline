#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Load Wikidata labels and hierarchy into Virtuoso triplestore

# ISSA environment definitions
. ../../../env.sh

log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/wikidata_import_$(date "+%Y%m%d_%H%M%S").log

# Start container if needed
CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME

# Remove previously imported ttl files
rm -f -v $WIKIDATA_IMPORT_DIR/wikidata-dump*.ttl 		   >>$log

cp -v wikidata-dump-en.ttl  $WIKIDATA_IMPORT_DIR              >>$log
cp -v wikidata-dump-fr.ttl  $WIKIDATA_IMPORT_DIR              >>$log
cp -v import-hierarchy.isql $WIKIDATA_IMPORT_DIR              >>$log

docker exec -w /database/import $CONTAINER_NAME \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD import-hierarchy.isql" -i $ISSA_NAMESPACE &>>$log



