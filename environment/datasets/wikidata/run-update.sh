#!/bin/bash

export ISSA_INSTANCE=$1

# ISSA environment definitions
. ../../../env.sh

echo "Backup previous data files"
backup_dir=./$ISSA_INSTANCE/bak/$(date "+%Y%m%d")
mkdir -p $backup_dir
cp -f ./$ISSA_INSTANCE/wikidata-*.txt $backup_dir
cp -f ./$ISSA_INSTANCE/wikidata-*.ttl $backup_dir

echo "Fetching URIs that don't have hierarchy yet..."
./retrieve-uris.sh

echo "Fetching hierarchies from Wikidata..."
./retrieve-hierarchy.sh     wikidata-dump-en.ttl    en
#./retrieve-hierarchy.sh     wikidata-dump-fr.ttl    fr

echo "Importing hierarchy in Virtuoso..."
./import-hierarchy.sh

echo "Move files to the instance directory..."
mkdir -p ./$ISSA_INSTANCE
mv -f ./wikidata-*.txt ./$ISSA_INSTANCE
mv -f ./wikidata-*.ttl ./$ISSA_INSTANCE
