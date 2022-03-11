#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Tune the variables in this file according to the environment

# URL for Agrovoc dump
# NOTE: this URL is a moving target
AGROVOC_URL=https://agrovoc.fao.org/agrovocReleases/agrovoc_2022-02-01_core.nt.zip
AGROVOC_GRAPH=http://agrovoc.fao.org/graph
AGROVOC_IMPORT_DIR=~/ISSA/volumes/virtuoso/database/import

# Version and release date of the Agritrop dataset being processed
#AGRITROP_VERSION=0
#AGRITROP_DATE=2021-06-07

# ISSA version (dot- and dashed-notation)
ISSA_VERSION=0.1
ISSA_VERSION_DASH=0-1

# ISSA dataset id 
export ISSA_DATA_ROOT=~/ISSA/data
export ISSA_DATASET=dataset-${ISSA_VERSION_DASH}
mkdir -p $ISSA_DATA_ROOT/$ISSA_DATASET
export LATEST_UPDATE=$(ls -Ar  --group-directories-first $ISSA_DATA_ROOT/$ISSA_DATASET | head -n 1) # doesn't work if the $ISSA_DATA_ROOT/$ISSA_DATASET does not exsist
export LATEST_UPDATE_DIR=$ISSA_DATA_ROOT/$ISSA_DATASET/$LATEST_UPDATE
export METADATA_PREFIX=agritrop_meta

DATASET_LANGUAGE=en #this is a default, can be overwritten in the scripts or not needed alltogether 
#CURRENT_DATE=$(date "+%Y-%m-%d") # potentially use this var to create a dataset version

# PDF storage
export PDF_CACHE=~/ISSA/data/pdf_cache 
export PDF_CACHE_UNREADBLE=$PDF_CACHE/unreadable

# Relative directory of ISSA metadata (tsv) 
ISSA_META=.

# Relative directory of ISSA Grobid extracted data (json) 
ISSA_FULLTEXT=json/coalesced

# Relative directory of DBpedia Spotlight annotations
ISSA_SPOTLIGHT=annotation/dbpedia-spotlight

# Relative directory of Entity-Fishing annotations 
ISSA_EF=annotation/entity-fishing

# Relative directory of Annif output
ISSA_ANNIF=indexing

# Relative directory of RDF output
ISSA_RDF=rdf

# Python virtual environment name and location
ISSA_VENV=~/ISSA/environment/python/issa_venv
export ISSA_SRC_ROOT=~/ISSA/pipeline 


# MongoDB database
DB=issa-latest
MONGODB_DATABASE_DIR=~/ISSA/volumes/mongodb
MONGODB_SOURCE_DIR=$ISSA_DATA_ROOT
MONGODB_IMPORT_DIR=$ISSA_SRC_ROOT/mongo

# xR2RML tool
XR2RML_TRANSFORMATION_DIR=$ISSA_SRC_ROOT/xR2RML

# Virtuoso 
VIRTUOSO_DATABASE_DIR=~/ISSA/volumes/virtuoso/database
VIRTUOSO_SOURCE_DIR=$ISSA_DATA_ROOT/$ISSA_DATASET/en/$ISSA_RDF # needs attention: language is hardcoded
VIRTUOSO_IMPORT_DIR=$ISSA_SRC_ROOT/virtuoso
VIRTUOSO_DEAFAULT_GRAPH=http://data-issa.cirad.fr/graph

# Annif
ANNIF_IMAGE=issa
ANNIF_PROJECTS_DIR=~/ISSA/volumes/annif-projects
ANNIF_SOURCE_DIR=$ISSA_DATA_ROOT/$ISSA_DATASET/en/indexing
ANNIF_TRAINING_DIR=$ISSA_DATA_ROOT/training
ANNIF_PROJECT=cirad-nn-ensemble-en
export ANNIF_SUFFIX=.parabel_mllm
ANNIF_LIMIT=15
ANNIF_THRESHOLD=0.1

# DBPedia-Spotlight
SPOTLIGHT_MODELS_DIR=~/ISSA/volumes/spotlight/models
SPOTLIGHT_LANGUAGES=en\ fr

# Wikidata Entity-Fishing
EF_MODELS_DIR=~/ISSA/volumes/entity-fishing/models
EF_LANGUAGES=en\ fr

