#!/bin/bash

export ISSA_INSTANCE=$1

# ISSA environment definitions
. ../../../env.sh

openalex_dump=openalex-topics-dump.ttl

echo "Backup previous data files"
backup_dir=./$ISSA_INSTANCE/bak/$(date "+%Y%m%d")
mkdir -p $backup_dir
cp -f ./$ISSA_INSTANCE/$openalex_dump   $backup_dir


echo "Fetching hierarchy from OpenAlex..."
./retrieve-hierarchy.sh     $openalex_dump

echo "Importing hierarchy in Virtuoso..."
./import-hierarchy.sh       $openalex_dump

echo "Move files to the instance directory..."
mkdir -p ./$ISSA_INSTANCE
mv -f ./$openalex_dump ./$ISSA_INSTANCE
