#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# 
# Load ISSA dataset metadata to the triplestore.

# ISSA environment definitions
. ../../env.sh

echo "namespace: $ISSA_NAMESPACE"
echo "input rdf dir: $VIRTUOSO_CONT_DATA_IMPORT_DIR"

log_dir=$ISSA_PIPELINE_LOG
mkdir -p $log_dir 
log=$log_dir/dataset_meta_import_$(date "+%Y%m%d_%H%M%S").log

# Copy dataset schema, provenance, and metadata with prefix substitution
sed "s#http://data-issa.instance.fr/#$ISSA_NAMESPACE#g" $DATASET_META_DIR/schema.ttl > $DATASET_META_IMPORT_DIR/schema.ttl
sed "s#http://data-issa.instance.fr/#$ISSA_NAMESPACE#g" $DATASET_META_DIR/provenance.ttl > $DATASET_META_IMPORT_DIR/provenance.ttl
sed "s#http://data-issa.instance.fr/#$ISSA_NAMESPACE#g" $DATASET_META_DIR/dataset.ttl > $DATASET_META_IMPORT_DIR/dataset.ttl


# Copy dataset metadata from the config directory if it is available there
if [ -f "$ISSA_PIPELINE_CONFIG/dataset.ttl" ]; then
    cp -v $ISSA_PIPELINE_CONFIG/dataset.ttl $DATASET_META_IMPORT_DIR &>> $log
fi


CONTAINER_NAME=${VIRTUOSO_CONT_NAME:-virtuoso}
docker start $CONTAINER_NAME

docker exec -w $VIRTUOSO_CONT_SCRIPT_DIR $CONTAINER_NAME \
   	       isql -H localhost -U dba -P $VIRTUOSO_PWD \
                 exec="LOAD ./import-dataset.isql" -i $VIRTUOSO_CONT_DATA_IMPORT_DIR $ISSA_NAMESPACE &>> $log

