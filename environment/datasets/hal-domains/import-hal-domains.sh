#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load GeoNmaes graph into Virtuoso triplestore

# ISSA environment definitions
. ../../../env.sh

log_dir=../../logs
mkdir -p $log_dir 
log=$log_dir/hal_domains_import_$(date "+%Y%m%d_%H%M%S").log

VIRTUOSO=${VIRTUOSO_CONT_NAME:-virtuoso}

docker start $VIRTUOSO

echo "Loading HAL domains..."                             >>$log

#rm -v "$HAL_DOMAINS_IMPORT_DIR"/*hal-domains*             >>$log

cp -v hal-domains-dump.ttl "$HAL_DOMAINS_IMPORT_DIR"     >>$log
cp -v import-hal-domains.isql  "$HAL_DOMAINS_IMPORT_DIR"     >>$log

docker exec $VIRTUOSO \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD /database/import/import-hal-domains.isql"   &>>$log

echo "done."                                                        >>$log