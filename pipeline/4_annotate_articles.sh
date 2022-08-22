#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA annotate text with DBPedia and Wikidata entities

# ISSA environment definitions
. ../env.sh

echo "Working on ${LATEST_UPDATE_DIR}"

source ${ISSA_VENV}/bin/activate

pushd ./ner

echo "************************************************************************"
echo "Annotate with DBPedia Spotlight..."
echo "************************************************************************"

for lang in $SPOTLIGHT_LANGUAGES; do
    echo "Starting dbpedia-spotlight.${lang}..."
    docker start dbpedia-spotlight.$lang
done

echo "Waiting for models to load (~2 min) ..."
sleep 2m
echo "Started dbpedia-spotlight.$SPOTLIGHT_LANGUAGES"

python3 ./annotation_dbpedia.py

for lang in $SPOTLIGHT_LANGUAGES; do
    echo "Stopping dbpedia-spotlight.${lang}"
    docker stop dbpedia-spotlight.$lang
done

echo "************************************************************************"
echo "Annotate with Wikidata Entity-Fishing..."
echo "************************************************************************"

echo "Starting entity-fishing..."
docker start entity-fishing

echo "Waiting for models to load (~1 min)..."
sleep 1m
echo "Started entity-fishing..."

python3 ./annotation_wikidata.py

echo "************************************************************************"
echo "Annotate with GeoNames by Entity-Fishing..."
echo "************************************************************************"

python3 ./annotation_geonames.py

echo "Stopping entity-fishing..."
docker stop entity-fishing

echo "************************************************************************"
echo "Annotate with Agrovoc Pyclinrec..."
echo "************************************************************************"

echo "Starting agrovoc-pyclinrec..."
docker start agrovoc-pyclinrec

echo "Waiting for recognizers to load (~10 sec)..."
sleep 10s
echo "Started agrovoc-pyclinrec..."

python3 ./annotation_agrovoc.py

docker stop agrovoc-pyclinrec


popd

deactivate
