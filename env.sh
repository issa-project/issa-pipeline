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
CURRENT_DATE=$(date "+%Y-%m-%d") # potentially use this var to create a dataset version
ISSA_VERSION=0.0
ISSA_VERSION_DASH=0-0

# ISSA dataset id (end of the dataset URI)
export ISSA_DATA_ROOT=~/ISSA/data
export ISSA_DATASET=dataset-${ISSA_VERSION_DASH}
export METADATA_PREFIX=agritrop
export DATASET_LANGUAGE=en #this is a default, can be overwritten in the scripts 
export ISSA_SRC_ROOT=~/ISSA/pipeline 

# Python virtual environment name and location
ISSA_VENV=~/ISSA/environment/python/issa_venv

# PDF storage
PDF_CACHE=~/ISSA/data/pdf_cache 


# Relative directory of ISSA metadata (tsv) 
ISSA_META=.

# Relative directory of ISSA Grobid extracted data (json) 
ISSA_FULLTEXT=json/coalesced

# Relative directory of DBpedia Spotlight annotations
ISSA_SPOTLIGHT=annotation/dbpedia-spotlight

# Relative directory of Entity-Fishing annotations 
ISSA_EF=annotation/entity-fishing

# Relative directory of RDF output
ISSA_RDF=rdf

# MongoDB database
DB=issa-latest
MONGODB_DATABASE_DIR=~/ISSA/volumes/mongodb
MONGODB_SOURCE_DIR=$ISSA_DATA_ROOT
MONGODB_IMPORT_DIR=$ISSA_SRC_ROOT/mongo

# xR2RML tool
XR2RML_TRANSFORMATION_DIR==$ISSA_SRC_ROOT/xR2RML

# Virtuoso 
VIRTUOSO_DATABASE_DIR=~/ISSA/volumes/virtuoso/database
VIRTUOSO_SOURCE_DIR=$ISSA_DATA_ROOT/$ISSA_DATASET/en/$ISSA_RDF # needs attention: language is hardcoded
VIRTUOSO_IMPORT_DIR=$ISSA_SRC_ROOT/virtuoso
VIRTUOSO_DEAFAULT_GRAPH=http://data-issa.cirad.fr/graph

#Annif
ANNIF_IMAGE=issa
ANNIF_PROJECTS_DIR=~/ISSA/volumes/annif-projects
ANNIF_SOURCE_DIR=$ISSA_DATA_ROOT/$ISSA_DATASET/en/indexing
ANNIF_PROJECT=cirad-mllm_en
ANNIF_SUFFIX=mllm

