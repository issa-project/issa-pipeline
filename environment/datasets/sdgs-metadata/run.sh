#!/bin/bash

export ISSA_INSTANCE=$1

# ISSA environment definitions
. ../../../env.sh

dump=sdgs-metadata.ttl


echo "Backup previous data files"
backup_dir=./$ISSA_INSTANCE/bak/$(date "+%Y%m%d")
mkdir -p $backup_dir
cp -f ./$ISSA_INSTANCE/$dump   $backup_dir


echo "Fecthing the SDG descriptions..."
python fetch_sdg_description.py


echo "Importing files in Virtuoso..."
./import.sh     $dump      import-sdgs-metadata.isql


echo "Move files to the instance directory..."
mkdir -p ./$ISSA_INSTANCE
mv -f ./$dump  ./$ISSA_INSTANCE
