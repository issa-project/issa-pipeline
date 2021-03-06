#!/bin/bash
#
# This script instantiates an xR2RML template file and runs Morph-xR2RML
# to produce the RDF annotations yield by Entity-Fishing.
#
# Input argument:
# - arg1: RDF dataset name e.g. "dataset-1-0"
# - arg2: article part about which to produce annotations. One of title, abstract or body_text
# - arg3: MongoDB collection to read data from
# - arg4: xR2RML template mapping file
# - arg5: output file name
#
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)

XR2RML=.
JAR=$XR2RML/morph-xr2rml-dist-1.3.2-20211126.142114-3-jar-with-dependencies.jar

help()
{
  exe=$(basename $0)
  echo "Usage: $exe <dataset name> <title|abstract|body_text> <collection> <xR2RML mapping template> <output file name>"
  echo "Example:"
  echo "   $exe  dataset-1-0  abstract  spotlight  xr2rml_spotlight_annot.tpl.ttl  issa-articles-spotlight-abstract.ttl"
  exit 1
}

# --- Read input arguments
dataset=$1
if [[ -z "$dataset" ]] ; then help; fi

articlepart=$2
if [[ -z "$articlepart" ]] ; then help; fi

collection=$3
if [[ -z "$collection" ]] ; then help; fi

mappingTemplate=$4
if [[ -z "$mappingTemplate" ]] ; then help; fi

output=$5
if [[ -z "$output" ]] ; then help; fi


# --- Init log file
log_dir=../logs 
mkdir -p $log_dir
log=$log_dir/run_xr2rml_${collection}_$(date "+%Y%m%d_%H%M%S").log
echo -n "" > $log

# --- Substitute placeholders in the xR2RML template file
mappingFile=/tmp/xr2rml_$$.ttl
awk "{ gsub(/{{dataset}}/, \"$dataset\"); \
       gsub(/{{articlepart}}/, \"$articlepart\"); \
       gsub(/{{collection}}/, \"$collection\"); \
       print }" \
    $XR2RML/${mappingTemplate} > $mappingFile
echo "-- xR2RML mapping file --" >> $log
cat $mappingFile >> $log


echo "--------------------------------------------------------------------------------------" >> $log
date  >> $log
java -Xmx24g \
     -Dlog4j.configuration=file:$XR2RML/log4j.properties \
     -jar "$JAR" \
     --configDir $XR2RML \
     --configFile xr2rml.properties \
     --mappingFile $mappingFile \
     --output $output \
     >> $log
date >> $log

rm -f $mappingFile
