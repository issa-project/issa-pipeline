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
  echo "Usage: $exe <database name> <collection> <index_column> <tsv file path> <additional script to run (optional)>"
  echo "Example:"
  echo "   $exe  dataset-1-0-20220202 document_metadata paper_id issa/data/dataset-1-0/20220202/document_meta.tsv aggregate_descriptors.js"
  exit 1
}

# --- Read input arguments
database=$1
if [[ -z "$database" ]] ; then help; fi

collection=$2
if [[ -z "$collection" ]] ; then help; fi

index_col=$3
if [[ -z "$index_col" ]] ; then help; fi

tsv_file=$4
if [[ -z "$tsv_file" ]] ; then help; fi

#optional
extra_script=$5
#if [[ -z "$extra_script" ]] ; then help; fi

# Functions definitions
. ./import-tools.sh

echo "Importing from $tsv_file"
echo "Importing to $collection in $database..."
echo "------------------------------------------------------------------------------"

mongo_drop_import_tsv $tsv_file $database $collection $index_col

#mongoimport --drop --type=tsv --headerline --ignoreBlanks -d $database -c $collection $tsv_file
#mongo --eval "db.${collection}.createIndex({${index_col}: 1})" localhost/$database --quiet


if [[ ! -z "$extra_script" ]] ; then

	echo "Executing additional script $extra_script..."
	echo "------------------------------------------------------------------------------"

	mongo localhost/$database "$extra_script" #--verbose   
fi





