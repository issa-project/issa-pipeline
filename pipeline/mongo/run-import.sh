#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../../env.sh

DB=$MONGODB_DB
WDIR=$MONGODB_CONT_SCRIPT_DIR
IDIR=$MONGODB_IMPORT_DIR	


log_dir=../logs 
mkdir -p $log_dir
log=$log_dir/import-mongodb_$(date "+%Y%m%d_%H%M%S").log


if [ $( docker ps -f name=mongodb | wc -l ) -gt 1 ]; then 

	docker exec -w $WDIR mongodb \
           ./import-tsv-file.sh $DB document_metadata agritrop_id $IDIR/$METADATA_PREFIX.tsv ./aggregate_descriptors.js &>> $log

	docker exec -w $WDIR mongodb \
           ./import-json-dir.sh $DB article_text paper_id $IDIR/$REL_FULLTEXT &>> $log

	docker exec -w $WDIR mongodb \
           ./import-json-dir.sh $DB annif_descriptors paper_id $IDIR/$REL_ANNIF &>> $log

	docker exec -w $WDIR mongodb \
           ./import-json-dir.sh $DB spotlight paper_id $IDIR/$REL_SPOTLIGHT &>> $log #lighten_spotlight.js 

	docker exec -w $WDIR mongodb \
           ./import-json-dir.sh $DB entityfishing paper_id $IDIR/$REL_EF &>> $log   #lighten_entityfishing_abstract.js

	docker exec -w $WDIR mongodb \
           ./import-json-dir.sh $DB geonames paper_id $IDIR/$REL_GEONAMES &>> $log   

fi

echo "done" >> $log








#	docker exec  -e DB=$MONGODB_DB \
#                 -e METADATA_PREFIX=$METADATA_PREFIX \
#                 -e LATEST_UPDATE_DIR=$MONGODB_LATEST_UPDATE \
#                 -e REL_FULLTEXT=$ISSA_FULLTEXT \
#                 -e REL_ANNIF=$REL_ANNIF \
#                 -e REL_SPOTLIGHT=$REL_SPOTLIGHT \
#                 -e REL_EF=$REL_EF \
#                 -e REL_GEONAMES=$REL_GEONAMES \
#                 -w /issa/import \
#			mongodb ./import-issa.sh &>> $log
