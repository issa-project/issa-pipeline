#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../../../env.sh

# Shorten var names for readability
DB=$MORPH_MONGODB_DB
SDIR=/issa/script
IDIR=/issa/data/$ISSA_INSTANCE/$ISSA_DATASET/$LATEST_UPDATE
WDIR=/mongo_tools

CONTAINER=${MONGO_XR2RML_CONT_NAME:-mongo-xr2rml}

log_dir=$ISSA_PIPELINE_LOG 
mkdir -p $log_dir
log=$log_dir/import_mongodb_$(date "+%Y%m%d_%H%M%S").log
echo "" > $log

echo "import database: $DB"
echo "import dir (container): $IDIR"
echo "script dir (container): $SDIR"

# Check if the Docker container is running
if [ $( docker ps -f name=$CONTAINER| wc -l ) -eq 1 ]; then
	echo "ERROR: $CONTAINER container is not running. Restart using docker-compose command." >> $log
	pushd $MORPH_XR2RML_DOCKER_COMPOSE_DIR >> $log 2>&1
		docker-compose start
     	sleep 5s
	popd
fi


docker exec -w $WDIR $CONTAINER \
           /bin/bash ./import-file.sh $IDIR/$METADATA_PREFIX.tsv tsv $DB document_metadata paper_id $SDIR/aggregate_descriptors.js >> $log 2>&1

docker exec -w $WDIR $CONTAINER \
           /bin/bash ./import-json-dir.sh $DB document_text paper_id $IDIR/$REL_FULLTEXT >> $log 2>&1

docker exec -w $WDIR $CONTAINER \
           ./import-json-dir.sh $DB annif_descriptors paper_id $IDIR/$REL_ANNIF >> $log 2>&1

docker exec -w $WDIR $CONTAINER \
           /bin/bash ./import-file.sh  $IDIR/$REL_OPENALEX/rao-stirling.json  json  $DB  rao_stirling  ISSA_Document_URI >> $log 2>&1

docker exec -w $WDIR $CONTAINER \
           /bin/bash ./import-json-dir.sh $DB spotlight paper_id $IDIR/$REL_SPOTLIGHT $SDIR/filter_spotlight.js >> $log 2>&1

docker exec -w $WDIR $CONTAINER \
           /bin/bash ./import-json-dir.sh $DB entityfishing paper_id $IDIR/$REL_EF $SDIR/filter_entityfishing.js >> $log 2>&1

docker exec -w $WDIR $CONTAINER \
           /bin/bash ./import-json-dir.sh $DB geonames paper_id $IDIR/$REL_GEONAMES $SDIR/filter_geonames.js >> $log 2>&1

docker exec -w $WDIR $CONTAINER \
           /bin/bash ./import-json-dir.sh $DB pyclinrec paper_id $IDIR/$REL_PYCLINREC $SDIR/filter_pyclinrec.js >> $log 2>&1

