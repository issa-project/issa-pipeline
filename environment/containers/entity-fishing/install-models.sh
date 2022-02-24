#!/bin/bash
# Authors: Anna BOBASHEVA, University Cote d'Azur, Inria
#          Andon Tchechmedjiev, EuroMov DHM, Université de Montpellier, IMT Mines Alès
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


# ISSA environment definitions
. ../../../env.sh


## Install the compiled indexed data

## Download the zipped data files for knowledge-base (Wikidata, db-kb.zip), 
## the English Wikipedia data (db-en.zip) and The French Wikipedia data (db-fr.zip)
## Current data version 0.0.4 correspond to the Wikidata and Wikipedia dumps from 20.05.2020.
## Total is around 29 GB compressed, and 97 GB uncompressed.

mkdir -p $EF_MODELS_DIR

pushd "$EF_MODELS_DIR"

wget https://science-miner.s3.amazonaws.com/entity-fishing/0.0.4/linux/db-kb.zip
unzip db-kb.zip

for lang in $EF_LANGUAGES; do
    wget https://science-miner.s3.amazonaws.com/entity-fishing/0.0.4/linux/db-$lang.zip
    unzip db-$lang.zip

## Unzip the db archives files 
## unziped files have to be mapped to data/db/ directory in the entity-fishing docker

rm *.zip

popd
