#!/bin/bash

echo "*************************************************"
echo " Backup previous data files"
echo "*************************************************"
mkdir -p ./bak/$(date "+%Y%m%d")
cp -f *.txt ./bak/$(date "+%Y%m%d")
cp -f *.ttl ./bak/$(date "+%Y%m%d")

echo "*************************************************"
echo " Fetching URIs that don't have hierarchy yet..."
echo "*************************************************"
./retrieve-uris.sh

echo "*************************************************"
echo " Fetching hierarchies from DBpedia..."
echo "*************************************************"
./retrieve-hierarchy.sh en
./retrieve-hierarchy.sh fr

echo "*************************************************"
echo " Fetching hierarchies from DBpedia..."
echo "*************************************************"
./import-hierarchy.sh




