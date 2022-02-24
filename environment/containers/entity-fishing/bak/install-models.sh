#!/bin/bash

## Install the compiled indexed data

## Download the zipped data files for knowledge-base (Wikidata, db-kb.zip), 
## the English Wikipedia data (db-en.zip) and The French Wikipedia data (db-fr.zip)
## Current data version 0.0.4 correspond to the Wikidata and Wikipedia dumps from 20.05.2020.
## Total is around 29 GB compressed, and 97 GB uncompressed.

cd ~/entity-fishing/models

wget https://science-miner.s3.amazonaws.com/entity-fishing/0.0.4/linux/db-kb.zip
wget https://science-miner.s3.amazonaws.com/entity-fishing/0.0.4/linux/db-en.zip
wget https://science-miner.s3.amazonaws.com/entity-fishing/0.0.4/linux/db-fr.zip

## Unzip the db archives files 
## unziped files have to be mapped to data/db/ directory in the entity-fishing docker

unzip db-kb.zip
unzip db-en.zip
unzip db-fr.zip

