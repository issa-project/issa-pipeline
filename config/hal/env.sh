#!/bin/bash
# Authors: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#          Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Tune the variables in this file according to the environment

# ISSA dataset nomenclature
ISSA_INSTANCE=hal
ISSA_VERSION=2.0                            		# version with dots 
ISSA_VERSION_DASH=2-0                       		# version with dashes
ISSA_NAMESPACE=http://data-issa.euromov.fr/ 	    # instance namespace
ISSA_DATASET_NAME=issa-hal-euromov      		    # this dataset name is used in the RDF dataset definition 

ISSA_ROOT=~/ISSA-2

###############################################################################
#                              PIPELINE
############################################################################### 

export ISSA_SRC_ROOT=$ISSA_ROOT/pipeline 
export ISSA_PIPELINE_CONFIG=$ISSA_ROOT/config/$ISSA_INSTANCE
export ISSA_PIPELINE_LOG=$ISSA_ROOT/pipeline/logs/$ISSA_INSTANCE 

# Python virtual environment name and location
export ISSA_VENV=~/ISSA-2/environment/python/issa_venv

###############################################################################
#                              DATA LOCATION
############################################################################### 

export ISSA_DATA_ROOT=$ISSA_ROOT/data/$ISSA_INSTANCE            # root of all data files
export ISSA_DATASET=dataset-${ISSA_VERSION_DASH} 

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
export REL_PYCLINREC=annotation/mesh      # Agrovoc annotations (use case specific vocabulary) 
export REL_RDF=rdf						# Relative directory of RDF output

# - dirs used for intermediate and debug files 
export REL_PDF=pdf						# document pdfs
export REL_GROBID_TXT                    # Grobid extracted data (txt) optional
export REL_GROBID_XML=xml				# Grobid extracted data (xml) optional
export REL_META_JSON=json/metadata		# text contained in metadata formatted as json 
export REL_GROBID_JSON=json/fulltext	     # text extracted by Grobid formatted as json
export REL_COAL_JSON=json/coalesced		# json coalesced from the two above with metadata replacing Grobit when present 


# Metadata configuration
export METADATA_PREFIX=$ISSA_INSTANCE.meta              # arbitrary metadata file name

# PDF storage
export PDF_CACHE=$ISSA_DATA_ROOT/pdf_cache            # location for PDF cache
export PDF_CACHE_UNREADABLE=$PDF_CACHE/unreadable 			 # separate the unreadable PDFs by Grobid here

# Dataset metadata
DATASET_META_DIR=$ISSA_ROOT/dataset
DATASET_META_IMPORT_DIR=$LATEST_UPDATE_DIR/$REL_RDF

###############################################################################
#                              ENVIRONMENT - CONTAINERS
############################################################################### 

ISSA_ENV_LOG=$ISSA_ROOT/environment/logs
#ISSA_MONGODB_TRANSIENT=true

# Morph-xR2RMLtools (docker container network)
export MORPH_XR2RML_DOCKER_COMPOSE_DIR=$ISSA_ROOT/environment/containers/morph-xr2rml
export MORPH_XR2RML_HOST_VOLUME=$ISSA_ROOT/volumes/morph-xr2rml
export MORPH_XR2RML_HOST_DATA_DIR=$ISSA_ROOT/data
export MORPH_XR2RML_CONT_DATA_DIR=/issa/data

# -- mongodb
export MONGO_XR2RML_CONT_NAME=mongo-xr2rml        # docker container name 
export MORPH_XR2RML_HOST_DATABASE_DIR=$MORPH_XR2RML_HOST_VOLUME/mongo_db
export MORPH_XR2RML_HOST_TOOLS_DIR=$MORPH_XR2RML_HOST_VOLUME/mongo_tools
export MORPH_XR2RML_HOST_SCRIPT_DIR=$ISSA_SRC_ROOT/morph-xr2rml/mongo 
export MORPH_XR2RML_CONT_SCRIPT_DIR=/issa/script      
export MORPH_MONGODB_DB=$ISSA_INSTANCE-$ISSA_VERSION_DASH-$LATEST_UPDATE

# -- xR2RML
export MORPH_XR2RML_CONT_NAME=morph-xr2rml        # docker container name
export MORPH_XR2RML_HOST_LOG_DIR=$ISSA_PIPELINE_LOG
export MORPH_XR2RML_HOST_TEMPL_DIR=$ISSA_SRC_ROOT/morph-xr2rml/xR2RML
export MORPH_XR2RML_CONT_TEMPL_DIR=/issa/template


# Virtuoso (docker container)
VIRTUOSO_CONT_NAME=virtuoso-$ISSA_INSTANCE                 # docker container name 
VIRTUOSO_HOST_ISQL_PORT=1112                     # local port for internal access to Virtuoso (1111 port)
VIRTUOSO_HOST_HTTP_PORT=8891				   # local port for http access to Virtuoso (8890 port)
VIRTUOSO_HOST_HTTPS_PORT=4444                    # local port for https access to Virtuoso (4443 port)
VIRTUOSO_DATABASE_DIR=$ISSA_ROOT/volumes/virtuoso-$ISSA_INSTANCE/database    # map to /database in the container FS for data persistency  
VIRTUOSO_IMPORT_DIR=$VIRTUOSO_DATABASE_DIR/import   # general purpose import dir is used for importing external datasets
VIRTUOSO_DEAFAULT_GRAPH=$ISSA_NAMESPACE/graph   # default graph name
VIRTUOSO_HOST_DATA_DIR=$ISSA_DATA_ROOT           # map host data dir

# IMPORTANT: VIRTUOSO_CONT_DATA_DIR has to be added to DirsAllowed in virtuoso.ini
VIRTUOSO_CONT_DATA_DIR=/issa/data                # to the container's FS to access data on the host. 
VIRTUOSO_HOST_SCRIPT_DIR=$ISSA_SRC_ROOT/virtuoso # map host script dir 
VIRTUOSO_CONT_SCRIPT_DIR=/issa/script            # to the container's FS to access scripts that have to be executed in the container 
VIRTUOSO_CONT_DATA_IMPORT_DIR=$VIRTUOSO_CONT_DATA_DIR/$ISSA_DATASET/$LATEST_UPDATE/$REL_RDF # path to the latest files to import 

# DBPedia-Spotlight (docker container)
SPOTLIGHT_CONT_NAME=dbpedia-spotlight                # docker container name
SPOTLIGHT_MODELS_DIR=$ISSA_ROOT/volumes/spotlight/models # map to /opt/spotlight/models in the container FS for data persistency
SPOTLIGHT_LANGUAGES=en\ fr                           # list of available language models

# Wikidata Entity-Fishing (docker container)
EF_CONT_NAME=entity-fishing                          # docker container name
EF_MODELS_DIR=$ISSA_ROOT/volumes/entity-fishing/models   # map to /opt/entity-fishing/data/db in the container FS for data persistency
EF_LANGUAGES=en\ fr                                  # list of available language models

# Pyclinrec concept recognizer with Agrovoc vocabulary (docker container)
PYCLINREC_CONT_NAME=pyclinrec                        # docker container name
PYCLINREC_HOST_CACHE=$ISSA_ROOT/volumes/pyclinrec/cache       # map to /app/cache dit on the container FS for dictionaries and recognizer objects persistency
PYCLINREC_DICT_ENDPOINT=http://data-issa.euromov.fr/sparql    # endpoint to SKOS vocabulary to create concept dictionary
PYCLINREC_DICT_GRAPH=http://id.nlm.nih.gov/mesh/graph         # endpoint graph name to restrict a vocabulary
PYCLINREC_DICT_NAME=mesh                             # endpoint graph name to restrict a vocabulary

###############################################################################
#                              ENVIRONMENT - EXTERNAL DATASETS IMPORT
############################################################################### 

# GeoNames dump
GEONAMES_DUMP_URL=https://download.geonames.org/all-geonames-rdf.zip # URL for Geonames RDF data dump
GEONAMES_GRAPH=http://geonames.org/graph         # graph name for GeoNames triples
GEONAMES_IMPORT_DIR=$VIRTUOSO_IMPORT_DIR         # copy Geonames RDF dump and import scripts to this dir for upload 

# Wikidata labels and hierarchies dump
WIKIDATA_IMPORT_DIR=$VIRTUOSO_IMPORT_DIR         # copy wikidata RDF dump and import scripts to this dir for upload 

# DBpedia labels and hierarchies dump
DBPEDIA_IMPORT_DIR=$VIRTUOSO_IMPORT_DIR           # copy DBpedia RDF dump and import scripts to this dir for upload 

###############################################################################
#                              ENVIRONMENT - INSTANCE SPECIFIC DATASETS
###############################################################################

# HAL domains thesaurus dump
HAL_DOMAINS_IMPORT_DIR=$VIRTUOSO_IMPORT_DIR      # copy HAL Domains RDF dump and import scripts to this dir for upload
HAL_DOMAINS_GRAPH_NAME=http://data.archives-ouvertes.fr/subject/graph 

# MESH descriptors thesaurus dump
MESH_URL=https://nlmpubs.nlm.nih.gov/projects/mesh/rdf/2022/mesh2022.nt.gz # URL for MESH RDF data dump
MESH_GRAPH_NAME=http://id.nlm.nih.gov/mesh/graph
MESH_IMPORT_DIR=$VIRTUOSO_IMPORT_DIR             # copy MESH  RDF dump and import scripts to this dir for upload 

