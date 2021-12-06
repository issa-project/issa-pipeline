#!/bin/bash
#

# Environment definitions
. ../env.sh

EN_RDF_DIR=$ISSA_DATA_ROOT/$ISSA_DATASET/en/$ISSA_RDF
FR_RDF_DIR=$ISSA_DATA_ROOT/$ISSA_DATASET/fr/$ISSA_RDF

# make import directories (if not exist)
mkdir -p $VIRTUOSO_IMPORT_DIR

# start docker (if not runing)

# probably some dir/file permissions have to change

# copy virtuoso.ini (if the first time)

# copy import.isql
cp -up import.isql $VIRTUOSO_IMPORT_DIR


# copy rdf data files
cp -up $EN_RDF_DIR/*.* $VIRTUOSO_IMPORT_DIR
cp -up $FR_RDF_DIR/*.* $VIRTUOSO_IMPORT_DIR

#Load the data
docker exec -d virtuoso isql -H localhost -U dba -P pass exec="LOAD /database/import/import.isql" 

# TODO: figure out where/how to log
#       fill the blanks above
