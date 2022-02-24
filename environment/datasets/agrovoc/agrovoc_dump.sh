#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA create metadata

# ISSA environment definitions
. ../../env.sh

log_dir=../logs
mkdir -p $log_dir 
current_time=$(date "+%Y%m%d_%H%M%S")
log_file=$log_dir/agrovoc_dump_${current_time}.log

#wget --no-check-certificate \
#     -o "$log_file" \
#     $AGROVOC_URL 

# get latest zip file
latest_dump=$(ls -rt *.zip | tail -n 1)
echo "$latest_dump"

rm -v "$AGROVOC_IMPORT_DIR"/agrovoc*.nt >>"$log_file"
#rm -v ./agrovoc*.nt >>"$log_file"

unzip -o "$latest_dump" -d "$AGROVOC_IMPORT_DIR" >>"$log_file"
#unzip -o "$latest_dump" -d ./ >>"$log_file"


