#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA create full text corpus

# ISSA environment definitions & export
. ../env.sh

PDF_CACHE=~/pdf_cache/$DATASET_LANGUAGE
PDF_DIR=${ISSA_DATA_ROOT}/${ISSA_DATASET}/${DATASET_LANGUAGE}/pdf

CURRENT_TIME=$(date "+%Y%m%d_%H%M%S")

# Try to copy from cache first
for f_url in ${PDF_DIR}/*.url; do
    f_pdf=${f_url/url/pdf}

	if [[ ! -f $f_pdf ]] ; then
		echo "$f_pdf not exists, try to copy from cache..."
		cp $PDF_CACHE/$(basename $f_pdf) $(dirname  $f_pdf) &>> ./logs/copy_pdf_${CURRENT_TIME}.log
	fi 
done


CURRENT_TIME=$(date "+%Y%m%d_%H%M%S")

# If file was not stored in cache then download from source
for f_url in ${PDF_DIR}/*.url; do
    f_pdf=${f_url/url/pdf}
	if [[ ! -f $f_pdf ]] ; then
		echo "$f_pdf not exists, downloading..."
		wget -nv -nc --tries=5 --no-use-server-timestamps -O $f_pdf -i $f_url -a ./logs/download_pdf_${CURRENT_TIME}.log 
   	    
	    cp $f_pdf $PDF_CACHE

		sleep 5
	fi 
done

# Copy Grobid-generated JSON files from cache
GROBID_CACHE=~/pdf_cache/$DATASET_LANGUAGE
GROBID_DIR=${ISSA_DATA_ROOT}/${ISSA_DATASET}/${DATASET_LANGUAGE}/json/fulltext
CURRENT_TIME=$(date "+%Y%m%d_%H%M%S")

rsynch -avu $GROBID_CACHE/*.json $GROBID_DIR &>> ./logs/copy_grobid_json_${CURRENT_TIME}.log


#for f_pdf in ${PDF_DIR}/*.pdf; do
#	f_txt=${f_pdf//pdf/pdftotxt}
#	if [[ ! -f $f_txt ]] ; then
#		echo "$f_txt not exists, extracting..."
#		pdftotext $f_pdf $f_txt
#	fi 
#done


source ${ISSA_VENV}/bin/activate

pushd ./fulltext
#COUNTER=10000
#CURRENT_TIME=$(date "+%Y%m%d_%H%M%S")

#for f_pdf in ${PDF_DIR}/*.pdf; do
#	f_json=${f_pdf//pdf/json}
#	f_json=${f_json/.json/.grobid.json}
#	if [[ ! -f $f_json ]] ; then
#		echo "$f_json not exists, extracting..."
#		python3 ./pdf_to_json.py $f_pdf --json=$f_json &>> ../logs/pdf_to_json_${CURRENT_TIME}.log
#		let COUNTER-=1 
#	fi
#        
#	if [  $COUNTER -eq 0 ]; then
#           break
#        fi  
#done

python3 ./pdf_to_json.py

python3 ./coalesce_meta_json.py

popd

deactivate

# Update Grobid cache
rsynch -avu $GROBID_DIR $GROBID_CACHE/*.json &>> ./logs/update_grobid_cache_${CURRENT_TIME}.log 
