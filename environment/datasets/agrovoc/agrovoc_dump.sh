#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Download the latest dump of Agrococ

# ISSA environment definitions
. ../../../env.sh

log_dir=../../logs
mkdir -p $log_dir 
log=$log_dir/agrovoc_dump_$(date "+%Y%m%d_%H%M%S").log

# create backup
mkdir -p bak
mv -f *.zip ./bak

echo "$AGROVOC_URL"
wget --no-check-certificate \
     -o "$log" \
     $AGROVOC_URL 

# get latest zip file
latest_dump=$(ls -rt *.zip | tail -n 1)
echo "latest dump file: $latest_dump"

# unzip directly to the Virtuoso's import dir
rm -v "$AGROVOC_IMPORT_DIR"/agrovoc*.nt          >>$log
unzip -o "$latest_dump" -d "$AGROVOC_IMPORT_DIR" >>$log


# unzip into this dir
#rm -v ./agrovoc*.nt 
#unzip -o "$latest_dump" -d ./                   


