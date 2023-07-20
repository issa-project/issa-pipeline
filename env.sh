#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Tune the variables in this file according to the environment

# ISSA version (dot- and dashed-notation)

# ISSA dataset nomenclature
ISSA_VERSION=1.2                             # version with dots 
ISSA_VERSION_DASH=1-2                        # version with dashes

export ISSA_DATA_ROOT=~/ISSA/data            # root of all data files
export ISSA_DATASET=dataset-${ISSA_VERSION_DASH} 
ISSA_DATASET_NAME=issa-agritrop              # this dataset name is used in the RDF dataset definition 

# Find the latest update folder 
# The latest update folder is created when the update repository is created in create_repository.py
mkdir -p $ISSA_DATA_ROOT/$ISSA_DATASET
export LATEST_UPDATE=$(ls -Ar  --group-directories-first $ISSA_DATA_ROOT/$ISSA_DATASET | head -n 1) 
export LATEST_UPDATE_DIR=$ISSA_DATA_ROOT/$ISSA_DATASET/$LATEST_UPDATE

# Directories of data files relative to the LATEST_UPDATE_DIR
# - dirs used downstream in the pipeline
export REL_META=.                            # metadata (tsv) 
export REL_FULLTEXT=json/coalesced	          # Grobid extracted data (json) 
export REL_SPOTLIGHT=annotation/dbpedia	     # DBpedia Spotlight annotations
export REL_EF=annotation/wikidata            # Entity-Fishing annotations 
export REL_GEONAMES=annotation/geonames	     # GeoNames annotations
export REL_PYCLINREC=annotation/agrovoc      # Agrovoc annotations (use case specific vocabulary) 
export REL_ANNIF=indexing				# Relative directory of Annif output
export REL_RDF=rdf						# Relative directory of RDF output

# - dirs used for intermediate and debug files 
export REL_ANNIF_LABELS=labels			# label tsv files for Annif training
export REL_ANNIF_TEXT=txt				# text files that can be used for ANNIF training
export REL_PDF=pdf						# document pdfs
export REL_GROBID_XML=xml				# Grobid extracted data (xml)
export REL_META_JSON=json/metadata		# text contained in metadata formatted as json 
export REL_GROBID_JSON=json/fulltext	# text extracted by Grobid formatted as json
export REL_COAL_JSON=json/coalesced		# json coalesced from the two above with metadata replacing Grobit when present 

# Python virtual environment name and location
ISSA_VENV=~/ISSA/environment/python/issa_venv
export ISSA_SRC_ROOT=~/ISSA/pipeline 

# Metadata configuration
export METADATA_PREFIX=agritrop_meta         # arbitrary metadata file name

# PDF storage
export PDF_CACHE=~/ISSA/data/pdf_cache            # location for PDF cache
export PDF_CACHE_UNREADABLE=$PDF_CACHE/unreadable # separate the unreadable PDFs by Grobid here

# MongoDB (docker container)
MONGODB_CONT_NAME=mongodb                        # docker container name 
MONGODB_HOST_PORT=27017					   # host port to the mongodb container	
MONGODB_DB=$ISSA_DATASET-$LATEST_UPDATE          # each data update is stored in a separate database in Mongo 
MONGODB_HOST_DATABASE_DIR=~/ISSA/volumes/mongodb # map to /data/db in the container FS for data persistency 
MONGODB_HOST_DATA_DIR=$ISSA_DATA_ROOT            # map host data dir
MONGODB_CONT_DATA_DIR=/issa/data                 # to the container's FS to access data on the host
MONGODB_HOST_SCRIPT_DIR=$ISSA_SRC_ROOT/mongo     # map host script dir
MONGODB_CONT_SCRIPT_DIR=/issa/script             # to the container's FS to access scripts that have to be executed in the container
MONGODB_IMPORT_DIR=$MONGODB_CONT_DATA_DIR/$ISSA_DATASET/$LATEST_UPDATE    # path to the latest files to import

# xR2RML tool
XR2RML_TRANSFORMATION_DIR=$ISSA_SRC_ROOT/xR2RML  # tool location   
XR2RML_OUTPUT_DIR=$LATEST_UPDATE_DIR/$REL_RDF    # output for generated RDF files

# Virtuoso (docker container)
VIRTUOSO_CONT_NAME=virtuoso                     # docker container name 
VIRTUOSO_DATABASE_DIR=~/ISSA/volumes/virtuoso/database    # map to /database in the container FS for data persistency    
VIRTUOSO_DEAFAULT_GRAPH=http://data-issa.cirad.fr/graph   # default graph name
VIRTUOSO_HOST_DATA_DIR=$ISSA_DATA_ROOT           # map host data dir
VIRTUOSO_CONT_DATA_DIR=/issa/data                # to the container's FS to access data on the host. IMPORTANT: The same dir has to be added to DirsAllowed in virtuoso.ini
VIRTUOSO_HOST_SCRIPT_DIR=$ISSA_SRC_ROOT/virtuoso # map host script dir 
VIRTUOSO_CONT_SCRIPT_DIR=/issa/script            # to the container's FS to access scripts that have to be executed in the container 
VIRTUOSO_IMPORT_DIR=$VIRTUOSO_CONT_DATA_DIR/$ISSA_DATASET/$LATEST_UPDATE/$REL_RDF # path to the latest files to import


# Annif (docker container)
ANNIF_IMAGE=original                             # obsolete 
ANNIF_CONT_NAME=annif                            # docker container name
ANNIF_PROJECTS_DIR=~/ISSA/volumes/annif-projects # map to /annif-projects in the container FS for data persistency
ANNIF_HOST_DATA_DIR=$ISSA_DATA_ROOT              # map host data dir
ANNIF_CONT_DATA_DIR=/issa/data                   # to the container's FS to access data on the host.
ANNIF_TRAINING_DIR=$ISSA_DATA_ROOT/training      # dir for Annif training data
ANNIF_INPUT_DIR=$ANNIF_CONT_DATA_DIR/$ISSA_DATASET/$LATEST_UPDATE/indexing # path to the latest files to process
ANNIF_PROJECT=cirad-nn-ensemble                  # name of the best model to use in indexing
export ANNIF_SUFFIX=.parabel_mllm_nn.tsv         # suffix to add to the indexing output file name and should correspond to the previous var
ANNIF_LIMIT=15                                   # max number of returned descriptors
ANNIF_THRESHOLD=0.1                              # confidence threshold of  returned descriptors
ANNIF_LANGUAGES=en\ fr                           # list of languages to process

# DBPedia-Spotlight (docker container)
SPOTLIGHT_CONT_NAME=dbpedia-spotlight                # docker container name
SPOTLIGHT_MODELS_DIR=~/ISSA/volumes/spotlight/models # map to /opt/spotlight/models in the container FS for data persistency
SPOTLIGHT_LANGUAGES=en\ fr                           # list of available language models

# Wikidata Entity-Fishing (docker container)
EF_CONT_NAME=entity-fishing                          # docker container name
EF_MODELS_DIR=~/ISSA/volumes/entity-fishing/models   # map to /opt/entity-fishing/data/db in the container FS for data persistency
EF_LANGUAGES=en\ fr                                  # list of available language models

# Pyclinrec concept recognizer with Agrovoc vocabulary (docker container)
PYCLINREC_CONT_NAME=agrovoc-pyclinrec                        # docker container name
PYCLINREC_DICT_ENDPOINT=https://data-issa.cirad.fr/sparql    # endpoint to SKOS vocabulary to create concept dictionary
PYCLINREC_DICT_GRAPH=http://agrovoc.fao.org/graph            # endpoint graph name to restrict a vocabulary
PYCLINREC_HOST_CACHE=~/ISSA/volumes/agrovoc-pyclinrec/cache  # map to /app/cache dit on the container FS for dictionaries and recognizer objects persistency

# Dataset metadata
DATASET_META_IMPORT_DIR=$VIRTUOSO_DATABASE_DIR/import # copy dataset metadata RDF files and import scripts to this dir for upload 

# External datasets import

# Agrovoc dump
AGROVOC_URL=https://agrovoc.fao.org/latestAgrovoc/agrovoc_core.nt.zip # URL for Agrovoc RDF data dump
AGROVOC_GRAPH=http://agrovoc.fao.org/graph 		   # graph name for Agrovoc triples
AGROVOC_IMPORT_DIR=$VIRTUOSO_DATABASE_DIR/import     # copy Agrovoc RDF dump and import scripts to this dir for upload 

# GeoNames dump
GEONAMES_DUMP_URL=https://download.geonames.org/all-geonames-rdf.zip # URL for Geonames RDF data dump
GEONAMES_GRAPH=http://geonames.org/graph             # graph name for GeoNames triples
GEONAMES_IMPORT_DIR=$VIRTUOSO_DATABASE_DIR/import    # copy geonames RDF dump and import scripts to this dir for upload 

# Wikidata labels and hierarchies dump
WIKIDATA_IMPORT_DIR=$VIRTUOSO_DATABASE_DIR/import    # copy wikidata RDF dump and import scripts to this dir for upload 

# DBpedia labels and hierarchies dump
DBPEDIA_IMPORT_DIR=$VIRTUOSO_DATABASE_DIR/import     # copy DBpedia RDF dump and import scripts to this dir for upload 

# AgrIST thesaurus
AGRIST_GRAPH=http://dist.cirad.fr/agrist-thema/graph  # graph name for AgrIST triples
AGRIST_IMPORT_DIR=$VIRTUOSO_DATABASE_DIR/import       # copy AgrIST RDF and import scripts to this dir for upload 

