#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# ISSA environment definitions
. ../../../env.sh

DB=$MORPH_MONGODB_DB
DROP_DB=${ISSA_MONGODB_TRANSIENT:-false}

CONTAINER=${MONGO_XR2RML_CONT_NAME:-mongo-xr2rml}

log_dir=$ISSA_PIPELINE_LOG 
mkdir -p $log_dir
log=$log_dir/drop_mongodb_$(date "+%Y%m%d_%H%M%S").log

if $DROP_DB ; then

	echo "drop database: $DB" >> $log

     stop_container=$( docker ps -f name=$CONTAINER| wc -l ) 

	docker start $CONTAINER

	docker exec $CONTAINER mongo $DB --eval "db.dropDatabase()" &>> $log

	if [ $stop_container -eq 1 ]; then 
		docker stop $CONTAINER
     fi
else
    echo "MongoDB data is set to be permanent. To change set ISSA_MONGODB_TRANSIENT=true in env.sh." >> $log
fi

