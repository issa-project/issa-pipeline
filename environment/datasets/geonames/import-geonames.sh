#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load GeoNmaes graph into Virtuoso triplestore

# ISSA environment definitions
. ../../../env.sh

log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/geonames_import_$(date "+%Y%m%d_%H%M%S").log


CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME

latest_rdf=$(ls -rt *.xml | tail -n 1)
echo "Loading $latest_rdf..."                                   >>$log

rm -v "$GEONAMES_IMPORT_DIR"/*geonames*                         >>$log

cp -v "$latest_rdf" "$GEONAMES_IMPORT_DIR"
cp -v import-geonames.isql "$GEONAMES_IMPORT_DIR"               >>$log

docker exec $CONTAINER_NAME \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD /database/import/import-geonames.isql"   &>>$log

echo "done."                                                     >>$log