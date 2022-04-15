#!/bin/bash
# Authors: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#          Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

# This script is presumed to run in MongoDB docker container with mapped volumes:
# issa/data - volume mapped to host's data directory containing all of the ISSA data 
# issa/import - volume mapped to host's directory for mongodb scripts 

help()
{
  exe=$(basename $0)
  echo "Usage: $exe <database name> <collection> <index_column> <dir path> <additional scripts to run (optional)>"
  echo "Example:"
  echo "   $exe  dataset-1-0-20220202 spotlight paper_id issa/data/dataset-1-0/20220202/annotation/dbpedia single lighten_spotlight.js"
  exit 1
}

# --- Read input arguments
database=$1
if [[ -z "$database" ]] ; then help; fi

collection=$2
if [[ -z "$collection" ]] ; then help; fi

index_col=$3
if [[ -z "$index_col" ]] ; then help; fi

json_dir=$4
if [[ -z "$json_dir" ]] ; then help; fi

#optional
extra_script=$5
#if [[ -z "$extra_script" ]] ; then help; fi


# Functions definitions
. ./import-tools.sh

echo "Importing from $json_dir"
echo "Importing to single $collection in $database..."
echo "------------------------------------------------------------------------------"


mongo_drop_import_dir $json_dir $database $collection $index_col

if [[ ! -z "$extra_script" ]] ; then

	echo "Executing additional script $extra_script..."
	echo "------------------------------------------------------------------------------"

	mongo localhost/$database "$extra_script" #--verbose   
fi



# delete down below this line


# ------------------------------------------------------------------------------

# Import the JSON files with Annif's suggestions
import_annif_desriptors() {
    collection=annif_descriptors
    echo "Importing $collection................................................."

    mongo_drop_import_dir $SOURCE/$REL_ANNIF $collection
}


# ------------------------------------------------------------------------------

# Import DBpedia-Spotlight annotations in a single collection
import_spotlight_single() {
    collection=spotlight
    echo "Importing $collection................................................."
    
    mongo_drop_import_dir $SOURCE/$REL_SPOTLIGHT $collection
    
    # Create collection spotlight_light 
    #mongo localhost/$DB lighten_spotlight.js
}


# Import Entity-fishing annotations in a single collection
import_entityfishing_single() {
    collection=entityfishing
    echo "Importing $collection................................................."
    
    mongo_drop_import_dir $SOURCE/$REL_EF $collection

    # Create lightened collection
    #mongo localhost/$DB lighten_entityfishing_abstract.js
}

# Import GeoNmanes annotations in a single collection
import_geonames_single() {
    collection=geonames

    mongo_drop_import_dir $SOURCE/$REL_GEONAMES $collection

}

# Import Entity-fishing annotations in a multiple collections
# NOTE: not used so far
import_entityfishing_multiple() {
    collection=entityfishing
    echo "Importing $collection................................................."
    
    mongo_drop_import_dir_split $SOURCE/$REL_EF $collection 30000

    # List the imported collections
    collections=$(mongo --eval "db.getCollectionNames()" $DB | sed 's|[",[:space:]]||g' | egrep "entityfishing_[[:digit:]]+")

    # Create a lightened collection for each collection just created
    for collection in $collections; do
        echo "----- Lightening collection $collection"
        sed "s|COLLECTION|$collection|g" lighten_entityfishing_body.js > lighten_entityfishing_body_tmp.js
        mongo localhost/$DB lighten_entityfishing_body_tmp.js
    done
    rm -f lighten_entityfishing_body_tmp.js
}




