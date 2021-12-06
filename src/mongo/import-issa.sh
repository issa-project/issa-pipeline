#!/bin/bash
# Authors: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#          Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# This script is presumed to run in MongoDB docker container with mapped volumes:
# source - root of local data directory containing all of the ISSA data 
# scripts - root of all scripts containing the environment definitions file env.sh 

SOURCE=./source
SCRIPTS=./scripts

# Environment definitions
. $SCRIPTS/env.sh

# Functions definitions
. $SCRIPTS/mongo/import-tools.sh


# ------------------------------------------------------------------------------

# Import metadata (agritrop_en.tsv or agritrop_fr.tsv)
#   $1: language 'en' or 'fr' 

import_issa_metadata() {
    # Metadata of all articles in the CORD19 dataset
    collection=metadata_$1
    mongoimport --drop --type=tsv --headerline --ignoreBlanks -d $DB -c $collection $SOURCE/$ISSA_DATASET/$1/${METADATA_PREFIX}_$1.tsv

    mongo --eval "db.${collection}.createIndex({paper_id: 1})" localhost/$DB
}

# Import the JSON files with Grobid extracted text
#   $1: language 'en' or 'fr' 
import_issa_json() {
    collection=fulltext_$1

    mongo_drop_import_dir $SOURCE/$ISSA_DATASET/$1/${ISSA_FULLTEXT} ${collection}

    # Create collection cord19_json_light
    #mongo localhost/$DB lighten_cord19json.js
}

# ------------------------------------------------------------------------------

# Import DBpedia-Spotlight annotations in a single collection
#   $1: language 'en' or 'fr' 
import_spotlight_single() {
    collection=spotlight_$1

    mongo_drop_import_dir $SOURCE/$ISSA_DATASET/$1/${ISSA_SPOTLIGHT} ${collection}
    
    # Create collection spotlight_light - IMHO thos should be handeled in the NER scripts
    #mongo localhost/$DB lighten_spotlight.js
}


# Import Entity-fishing annotations in a single collection
#   $1: language 'en' or 'fr' 
import_entityfishing_single() {
    collection=entityfishing_$1

    mongo_drop_import_dir $SOURCE/$ISSA_DATASET/$1/${ISSA_EF} ${collection}

    # Create lightened collection
    #mongo localhost/$DB lighten_entityfishing_abstract.js
}


# Import Entity-fishing annotations in a multiple collections
import_entityfishing_multiple() {
    collection=entityfishing
    mongo_drop_import_dir_split ${CORD19_EF} ${collection} 30000

    # List the imported collections
    collections=$(mongo --eval "db.getCollectionNames()" cord19v47 | sed 's|[",[:space:]]||g' | egrep "entityfishing_[[:digit:]]+")

    # Create a lightened collection for each collection just created
    for collection in $collections; do
        echo "----- Lightening collection $collection"
        sed "s|COLLECTION|$collection|g" lighten_entityfishing_body.js > lighten_entityfishing_body_tmp.js
        mongo localhost/$DB lighten_entityfishing_body_tmp.js
    done
    rm -f lighten_entityfishing_body_tmp.js
}


import_issa_metadata $DATASET_LANGUAGE
import_issa_json $DATASET_LANGUAGE
import_spotlight_single $DATASET_LANGUAGE
import_entityfishing_single $DATASET_LANGUAGE
