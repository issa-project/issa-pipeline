#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load Wikidatad lables and hierarchy into Virtuoso triplestore

# ISSA environment definitions
. ../../../env.sh

log_dir=../../logs
mkdir -p $log_dir 
log=$log_dir/wikidata_import_$(date "+%Y%m%d_%H%M%S").log

docker start virtuoso

# Remove previously imported ttl files
rm -f -v "$WIKIDATA_IMPORT_DIR"/wikidata-dump*.ttl 				>>$log

cp -v wikidata-dump-en.ttl "$WIKIDATA_IMPORT_DIR"              >>$log
cp -v wikidata-dump-fr.ttl "$WIKIDATA_IMPORT_DIR"              >>$log
cp -v import-hierarchy.isql "$WIKIDATA_IMPORT_DIR"              >>$log

docker exec virtuoso \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD /database/import/import-hierarchy.isql"    &>>$log



