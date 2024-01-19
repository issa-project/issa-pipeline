#!/bin/bash

export ISSA_INSTANCE=$1

# ISSA environment definitions
. ../../../env.sh

echo "*************************************************"
echo " Backup previous data files"
echo "*************************************************"
backup_dir=./$ISSA_INSTANCE/bak/$(date "+%Y%m%d")
mkdir -p $backup_dir
cp -f ./$ISSA_INSTANCE/wikidata-*.txt $backup_dir
cp -f ./$ISSA_INSTANCE/wikidata-*.ttl $backup_dir

echo "*************************************************"
echo " Fetching URIs that don't have hierarchy yet..."
echo "*************************************************"
./retrieve-uris.sh

echo "*************************************************"
echo " Fetching hierarchies from Wikidata..."
echo "*************************************************"
./retrieve-hierarchy.sh query-hierarchy.sparql           wikidata-dump-en.ttl           en
./retrieve-hierarchy.sh query-hierarchy.sparql           wikidata-dump-fr.ttl           fr
./retrieve-hierarchy.sh query-hierarchy-inferred.sparql  wikidata-dump-inferred-en.ttl  en
./retrieve-hierarchy.sh query-hierarchy-inferred.sparql  wikidata-dump-inferred-fr.ttl  fr

echo "*************************************************"
echo " Fetching hierarchies from Wikidata..."
echo "*************************************************"
./import-hierarchy.sh

echo "*************************************************"
echo " Move files to the instance directory..."
echo "*************************************************"
mkdir -p ./$ISSA_INSTANCE
mv -f ./wikidata-*.txt ./$ISSA_INSTANCE
mv -f ./wikidata-*.ttl ./$ISSA_INSTANCE


