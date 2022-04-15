#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA index documents with Annif tool

# ISSA environment definitions
. ../../env.sh

IDIR=$ANNIF_INPUT_DIR

echo "Indexing documents in ${IDIR}..."

docker start annif


for lang in $ANNIF_LANGUAGES; do

	log_dir=../logs 
	mkdir -p $log_dir
	log=$log_dir/annif-indexing_"$lang"_$(date "+%Y%m%d_%H%M%S").log

	if [ $( docker ps -f name=annif | wc -l ) -gt 1 ]; then 
	    	docker exec annif annif index \
                         --suffix $ANNIF_SUFFIX \
    					  --force \
                         --limit $ANNIF_LIMIT \
                         --threshold $ANNIF_THRESHOLD \
                         $ANNIF_PROJECT-$lang \
    					  $IDIR/$lang | tee $log
    fi

done 

docker stop annif
