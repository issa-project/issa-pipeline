#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Download the latest MESH thesaurus dump

# ISSA environment definitions
. ../../../env.sh


log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/mesh_dump_$(date "+%Y%m%d_%H%M%S").log

# create backup
mkdir -p bak
mv -f *.nt ./bak

echo "$MESSH_URL"
wget --no-check-certificate \
     -o "$log" \
     $MESH_URL   


# get latest zip file
latest_dump=$(ls -rt *.gz | tail -n 1)
echo "latest dump file: $latest_dump"   						>>$log
echo "destination file ${MESH_IMPORT_DIR}/${latest_dump%.gz}"   >>$log


# unzip directly to the Virtuoso's import dir
rm -v "$MESH_IMPORT_DIR"/mesh*.nt          					>>$log
gzip -dc "$latest_dump" > "$MESH_IMPORT_DIR/${latest_dump%.gz}" >>$log

             
