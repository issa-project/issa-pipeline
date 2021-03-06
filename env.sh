#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Tune the variables in this file according to the environment

# Agrovoc dump
AGROVOC_URL=https://agrovoc.fao.org/latestAgrovoc/agrovoc_core.nt.zip
AGROVOC_GRAPH=http://agrovoc.fao.org/graph
AGROVOC_IMPORT_DIR=~/ISSA/volumes/virtuoso/database/import

# GeoNames dump
GEONAMES_DUMP_URL=https://download.geonames.org/all-geonames-rdf.zip
GEONAMES_GRAPH=http://geonames.org/graph 
GEONAMES_IMPORT_DIR=~/ISSA/volumes/virtuoso/database/import

# ISSA version (dot- and dashed-notation)
ISSA_VERSION=1.0
ISSA_VERSION_DASH=1-0

# ISSA dataset id 
export ISSA_DATA_ROOT=~/ISSA/data
export ISSA_DATASET=dataset-${ISSA_VERSION_DASH}

mkdir -p $ISSA_DATA_ROOT/$ISSA_DATASET
export LATEST_UPDATE=$(ls -Ar  --group-directories-first $ISSA_DATA_ROOT/$ISSA_DATASET | head -n 1) # doesn't work if the $ISSA_DATA_ROOT/$ISSA_DATASET does not exsist
export LATEST_UPDATE_DIR=$ISSA_DATA_ROOT/$ISSA_DATASET/$LATEST_UPDATE

# potentially use this var to create a dataset version
#CURRENT_DATE=$(date "+%Y-%m-%d") 

export METADATA_PREFIX=agritrop_meta

# PDF storage
export PDF_CACHE=~/ISSA/data/pdf_cache 
export PDF_CACHE_UNREADBLE=$PDF_CACHE/unreadable

# Directories of data files relative to LATEST_UPDATE_DIR
# - dirs used downstream in the pipeline
export REL_META=.    					# metadata (tsv) 
export REL_FULLTEXT=json/coalesced		# Grobid extracted data (json) 
export REL_SPOTLIGHT=annotation/dbpedia	# DBpedia Spotlight annotations
export REL_EF=annotation/wikidata		# Entity-Fishing annotations 
export REL_GEONAMES=annotation/geonames	# GeoNames annotations 
export REL_ANNIF=indexing				# Relative directory of Annif output
export REL_RDF=rdf						# Relative directory of RDF output

# - dirs used for intermediate and debug files 
export REL_ANNIF_LABELS=lables			# label tsv files for Annif training
export REL_ANNIF_TEXT=txt				# text files that can be used for ANNIF trainig
export REL_PDF=pdf						# document pdfs
export REL_GROBID_XML=xml				# Grobid extracted data (xml)
export REL_META_JSON=json/metadata		# text contained in metadata formated as json 
export REL_GROBID_JSON=json/fulltext	# text extracted by Grobid formated as json
export REL_COAL_JSON=json/coalesced		# json coalesced from the two above with metadata replacing Grobit when present 
                               

# Python virtual environment name and location
ISSA_VENV=~/ISSA/environment/python/issa_venv
export ISSA_SRC_ROOT=~/ISSA/pipeline 


# MongoDB 
MONGODB_HOST_DATABASE_DIR=~/ISSA/volumes/mongodb # maps to /data/db
MONGODB_HOST_DATA_DIR=$ISSA_DATA_ROOT
MONGODB_CONT_DATA_DIR=/issa/data
MONGODB_HOST_SCRIPT_DIR=$ISSA_SRC_ROOT/mongo
MONGODB_CONT_SCRIPT_DIR=/issa/script
MONGODB_IMPORT_DIR=$MONGODB_CONT_DATA_DIR/$ISSA_DATASET/$LATEST_UPDATE
MONGODB_DB=$ISSA_DATASET-$LATEST_UPDATE

# xR2RML tool
XR2RML_TRANSFORMATION_DIR=$ISSA_SRC_ROOT/xR2RML
XR2RML_OUTPUT_DIR=$LATEST_UPDATE_DIR/$REL_RDF

# Virtuoso 
VIRTUOSO_DATABASE_DIR=~/ISSA/volumes/virtuoso/database
VIRTUOSO_DEAFAULT_GRAPH=http://data-issa.cirad.fr/graph
#####VIRTUOSO_HOST_DATA_DIR=/home/issa/ISSA/data/dataset-0-0/en/$REL_RDF 
VIRTUOSO_HOST_DATA_DIR=$ISSA_DATA_ROOT
VIRTUOSO_CONT_DATA_DIR=/issa/data                        #IMPORTANT: The same dir has to be added to DirsAllowed in virtuoso.ini
VIRTUOSO_HOST_SCRIPT_DIR=$ISSA_SRC_ROOT/virtuoso
VIRTUOSO_CONT_SCRIPT_DIR=/issa/script
VIRTUOSO_IMPORT_DIR=$VIRTUOSO_CONT_DATA_DIR/$ISSA_DATASET/$LATEST_UPDATE/$REL_RDF


# Annif
ANNIF_IMAGE=issa
ANNIF_PROJECTS_DIR=~/ISSA/volumes/annif-projects
ANNIF_HOST_DATA_DIR=$ISSA_DATA_ROOT
ANNIF_CONT_DATA_DIR=/issa/data
ANNIF_TRAINING_DIR=$ISSA_DATA_ROOT/training
ANNIF_INPUT_DIR=$ANNIF_CONT_DATA_DIR/$ISSA_DATASET/$LATEST_UPDATE/indexing
ANNIF_PROJECT=cirad-nn-ensemble
export ANNIF_SUFFIX=.parabel_mllm_nn
ANNIF_LIMIT=15
ANNIF_THRESHOLD=0.1
ANNIF_LANGUAGES=en\ fr

# DBPedia-Spotlight
SPOTLIGHT_MODELS_DIR=~/ISSA/volumes/spotlight/models
SPOTLIGHT_LANGUAGES=en\ fr

# Wikidata Entity-Fishing
EF_MODELS_DIR=~/ISSA/volumes/entity-fishing/models
EF_LANGUAGES=en\ fr

# Dataset
DATASET_META_IMPORT_DIR=~/ISSA/volumes/virtuoso/database/import

# Lables and hierarchies 
WIKIDATA_IMPORT_DIR=~/ISSA/volumes/virtuoso/database/import
DBPEDIA_IMPORT_DIR=~/ISSA/volumes/virtuoso/database/import
