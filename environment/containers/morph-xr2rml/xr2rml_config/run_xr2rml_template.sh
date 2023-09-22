#!/bin/bash
#
# This script runs Morph-xR2RML in graph materialization mode,
# that is it applies the mappings and outputs the corresponding RDF file.
# It first replaces the placeholders in the template mapping file.
# Adapted to the templates specific for the ISSA project
#
# Input argument:
# - arg1: xR2RML template mapping file. 
# - arg2: output file name 
# - arg3: database name (optional) replacement of database parameter in xr2rml.properties file 
# - arg4: replacement of the MongoDB collection parameter {{collection}} the mapping template, e.g. metadata
# - arg5: replacement of the dataset parameter {{dataset}} in the mapping template, e.g. "dataset1"
# - arg6: replacement of the dataset parameter {{namespace}} in the mapping template, e.g. "http://data-issa.ciradf.fr/"
# - arg7: replacement of the dataset parameter {{documentpart}} in the mapping template, e.g. "title" for splitting the large number of annottations
#
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#         Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

XR2RML=/morph-xr2rml
CONFIG_DIR=/xr2rml_config
LOG_DIR=/log
OUTPUT_DIR=/xr2rml_output

JAR=$XR2RML/morph-xr2rml-dist-1.3.2-20211126.142114-3-jar-with-dependencies.jar


help()
{
  exe=$(basename $0)
  echo "Usage: $exe <xR2RML mapping template> <output file name> <MongoDB collection name> [dataset name] [namespace for dataset-specific IRIs] [title|abstract|body_text]"
  echo "Example:"
  echo "   $exe template/xr2rml_spotlight_annot.tpl.ttl  output/issa-documents-spotlight-abstract.ttl database document_metadata dataset-1-0 http://data-issa.ciradf.fr/"

  exit 1
}

# --- Read input arguments
mappingTemplate=$1
if [[ -z "$mappingTemplate" ]] ; then help; fi

output=$2
if [[ -z "$output" ]] ; then help; fi

database=$3
#if [[ -z "$database" ]] ; then help; fi

collection=$4
#if [[ -z "$collection" ]] ; then help; fi

dataset=$5
#if [[ -z "$dataset" ]] ; then help; fi

namespace=$6
#if [[ -z "$namespace" ]] ; then help; fi

documentpart=$7
#if [[ -z "$documentpart" ]] ; then help; fi


# --- Init log file
mkdir -p $LOG_DIR
log=$LOG_DIR/xr2rml_${collection}_$(date "+%Y%m%d_%H%M%S").log

# --- Change the Mongo database name in the xr2rml.properties 
if [[ ! -z "$database" ]] ; then 
   echo "Setting database to $database"
   sed -i "/^database.name\[0\]=/s/=.*/=$database/" xr2rml.properties
fi

# --- Substitute placeholders in the xR2RML template mapping
mappingFile=/tmp/xr2rml_$$.ttl
awk "{ gsub(/{{collection}}/, \"$collection\"); \
	  gsub(/{{dataset}}/, \"$dataset\"); \
       gsub(/{{namespace}}/, \"$namespace\"); \
       gsub(/{{documentpart}}/, \"$documentpart\"); \
       print }" \
       ${mappingTemplate} > $mappingFile
echo "-- xR2RML mapping file --" >> $log
cat $mappingFile >> $log


echo "--------------------------------------------------------------------------------------" >> $log
date  >> $log
java -Xmx4g \
     -Dlog4j.configuration=file:$CONFIG_DIR/log4j.properties \
     -jar "$JAR" \
     --configDir $CONFIG_DIR \
     --configFile xr2rml.properties \
     --mappingFile $mappingFile \
     --output $output \
     >> $log
date >> $log

rm -f $mappingFile
