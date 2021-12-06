#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Tune the variables in this file according to the environment


# Version and release date of the Agritrop dataset being processed
AGRITROP_VERSION=0
AGRITROP_DATE=2021-06-07

# ISSA version (dot- and dashed-notation)
ISSA_VERSION=0.0
ISSA_VERSION_DASH=0-0

# ISSA dataset id (end of the dataset URI)
export ISSA_DATA_ROOT=~/data
export ISSA_DATASET=dataset-${ISSA_VERSION_DASH}
export METADATA_PREFIX=agritrop
export DATASET_LANGUAGE=en
export ISSA_SRC_ROOT=~/src

# Python virtual environment name and location
ISSA_VENV=${ISSA_SRC_ROOT}/issa_venv

# Directory of ISSA metadata (tsv) 
#CORD19_DIR=/appli/cord19/CORD-19-V${CORD19_VERSION}
#ISSA_DIR=~/data
ISSA_META=.

# Reative directory of ISSA Grobid extracted data (json)
#CORD19_DIR=/appli/cord19/CORD-19-V${CORD19_VERSION}
ISSA_FULLTEXT=json/coalesced

# Relative directory of DBpedia Spotlight annotations (unzipped)
#CORD19_SPOTLIGHT=/appli/cord19/CORD-19-V${CORD19_VERSION}-Annotation/dbpedia-spotlight
ISSA_SPOTLIGHT=annotation/dbpedia-spotlight

# Relative directory of Entity-Fishing annotations (unzipped)
#CORD19_EF=/appli/cord19/CORD-19-V${CORD19_VERSION}-Annotation/entity-fishing
ISSA_EF=annotation/entity-fishing

# Relative directory of RDF output
ISSA_RDF=rdf


# MongoDB database
MONGODB_CONTAINER=true
DB=issa-latest

# Virtuoso 
VIRTUOSO_DATABASE_VOLUME_DIR=~/virtuoso/database
VIRTUOSO_IMPORT_DIR=$VIRTUOSO_DATABASE_VOLUME_DIR/import
VIRTUOSO_DEAFAULT_GRAPH=http://data-issa.cirad.fr/graph

########################################################
# Franck's environment variables

export DATASET_VERSION=1.0
export DATASET_VERSION_DASH=1-0
export DATASET_DATE=2021-01-01

# MongoDB database
#export DB=issa

# Dataset id (end of the dataset URI)
export DATASET_ID=dataset-${DATASET_VERSION_DASH}