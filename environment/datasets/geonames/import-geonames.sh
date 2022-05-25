#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Load GeoNmaes graph into Virtuoso triplestore

# ISSA environment definitions
. ../../../env.sh

log_dir=../../logs
mkdir -p $log_dir 
log=$log_dir/geonames_import_$(date "+%Y%m%d_%H%M%S").log

docker strat virtuoso

latest_rdf=$(ls -rt *.xml | tail -n 1)
echo "Loading $latest_rdf..."                                   >>$log

rm -v "$GEONAMES_IMPORT_DIR"/*geonames*                         >>$log

cp -v "$latest_rdf" "$GEONAMES_IMPORT_DIR"
cp -v import-geonames.isql "$GEONAMES_IMPORT_DIR"               >>$log

docker exec virtuoso \
            isql -H localhost -U dba -P $VIRTUOSO_PWD \
            exec="LOAD /database/import/import-geonames.isql"   &>>$log

echo "done."                                                     >>$log