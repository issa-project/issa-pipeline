#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA index documents with Annif tool

# ISSA environment definitions
. ../../env.sh

IDIR=$ANNIF_INPUT_DIR

docker start annif

log_dir=../logs 
mkdir -p $log_dir
log=$log_dir/indexing_annif_$(date "+%Y%m%d_%H%M%S").log

echo "Indexing documents in ${IDIR}..."                              >> $log

for lang in $ANNIF_LANGUAGES; do

    echo "Indexing $lang documents..."                               >> $log

	if [ $( docker ps -f name=annif | wc -l ) -gt 1 ]; then 
	    	docker exec annif annif index \
                         --suffix $ANNIF_SUFFIX \
    					  --force \
                         --limit $ANNIF_LIMIT \
                         --threshold $ANNIF_THRESHOLD \
                         $ANNIF_PROJECT-$lang \
    					  $IDIR/$lang                                &>> $log
    fi

done 

docker stop annif
