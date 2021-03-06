#!/bin/bash
#
# This script runs Morph-xR2RML to produce the RDF version of the CORD19 metadata.csv file
#
# Input argument:
# - arg1: RDF dataset name e.g. "dataset-1-0"
# - arg2: the MongoDB collection to query, e.g. document_metadata
# - arg3: xR2RML template mapping file
# - arg4: output file 
#
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

XR2RML=.
JAR=$XR2RML/morph-xr2rml-dist-1.3.2-20211126.142114-3-jar-with-dependencies.jar

help()
{
  exe=$(basename $0)
  echo "Usage: $exe <dataset name> <MongoDB collection name> <pmcid|sha> <xR2RML mapping template> <output file name>"
  echo "Example:"
  echo "   $exe  dataset-1-0  document_metadata  xr2rml_document_metadata.tpl.ttl  issa-articles-metadata.ttl"
  exit 1
}

# --- Read input arguments
dataset=$1
if [[ -z "$dataset" ]] ; then help; fi

collection=$2
if [[ -z "$collection" ]] ; then help; fi

mappingTemplate=$3
if [[ -z "$mappingTemplate" ]] ; then help; fi

output=$4
if [[ -z "$output" ]] ; then help; fi


# --- Init log file
log_dir=../logs 
mkdir -p $log_dir
log=$log_dir/run_xr2rml_${collection}_$(date "+%Y%m%d_%H%M%S").log


# --- Substitute placeholders in the xR2RML template file
mappingFile=/tmp/xr2rml_$$.ttl
awk "{ gsub(/{{dataset}}/, \"$dataset\"); \
       gsub(/{{collection}}/, \"$collection\"); \
       print }" \
    $XR2RML/${mappingTemplate} > $mappingFile
echo "-- xR2RML mapping file --" >> $log
cat $mappingFile >> $log


echo "--------------------------------------------------------------------------------------" >> $log
date  >> $log
java -Xmx4g \
     -Dlog4j.configuration=file:$XR2RML/log4j.properties \
     -jar "$JAR" \
     --configDir $XR2RML \
     --configFile xr2rml.properties \
     --mappingFile $mappingFile \
     --output $output \
     >> $log
date >> $log

rm -f $mappingFile
