
#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Annotate text with DBPedia and Wikidata entities

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

python3 ./annotation_dbpedia.py $ISSA_PIPELINE_CONFIG


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

python3 ./annotation_wikidata.py $ISSA_PIPELINE_CONFIG

echo "************************************************************************"
echo "Annotate with GeoNames by Entity-Fishing..."
echo "************************************************************************"

python3 ./annotation_geonames.py $ISSA_PIPELINE_CONFIG

echo "Stopping entity-fishing..."
docker stop entity-fishing

echo "************************************************************************"
echo "Annotate with a custom dictionary and Pyclinrec..."
echo "************************************************************************"

echo "Starting pyclinrec..."
docker start pyclinrec

echo "Waiting for recognizers to load (~1 min)..."
sleep 1m
echo "Started pyclinrec..."

python3 ./annotation_pyclinrec.py  $ISSA_PIPELINE_CONFIG

docker stop pyclinrec


echo "************************************************************************"
echo "Detect overlapping named entities..."
echo "************************************************************************"

python3 ./overlap_detection.py $ISSA_PIPELINE_CONFIG

popd

deactivate
