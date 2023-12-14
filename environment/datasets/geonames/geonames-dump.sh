#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Download the latest dump of GeoNames graph 

# ISSA environment definitions
. ../../../env.sh

log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/geonames_dump_$(date "+%Y%m%d_%H%M%S").log

# create backup
mkdir -p bak
mv -f *.zip ./bak
#mv -f *.txt ./bak
#mv -f *.xml ./bak

echo "Getting geonames from $GEONAMES_DUMP_URL..."

wget --no-check-certificate \
     -o "$log" \
     $GEONAMES_DUMP_URL

# get latest zip file
latest_dump=$(ls -rt *.zip | tail -n 1)
echo "latest dump zip: $latest_dump"

unzip -o "$latest_dump" -d ./ &>>$log

# TODO: refactor reformat_geonames_rdf_dump to output progress log
#       take an input and output files as parameters

source ${ISSA_VENV}/bin/activate
python3 reformat_geonames_rdf_dump.py &>>$log
deactivate

latest_rdf=$(ls -rt *.xml | tail -n 1)
echo "latest dump xml: $latest_rdf"

# remove large file if needed
# rm -v ./all-geonames-rdf.txt


 



