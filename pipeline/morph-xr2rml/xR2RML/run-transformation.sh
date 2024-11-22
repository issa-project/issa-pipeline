#!/bin/bash
# Authors: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#        : Anna BOBASHEVA, University Cote d'Azur, Inria

# ISSA environment definitions
. ../../../env.sh


# Shorten var names for readability
DB=$MORPH_MONGODB_DB
TDIR=/issa/template
ODIR=/issa/data/$ISSA_INSTANCE/$ISSA_DATASET/$LATEST_UPDATE/$REL_RDF
WDIR=/xr2rml_config

DS=$ISSA_DATASET_NAME
NS=$ISSA_NAMESPACE

CONTAINER=${MORPH_XR2RML_CONT_NAME:-morph-xr2rml}

echo "input database: $DB"
echo "output rdf dir (host): $LATEST_UPDATE_DIR/$REL_RDF"
echo "output rdf dir (container): $ODIR"

# Make a directory where the output files will be stored
mkdir -p $LATEST_UPDATE_DIR/$REL_RDF 

log_dir=$ISSA_PIPELINE_LOG 
mkdir -p $log_dir
log=$log_dir/transform_xR2RML_$(date "+%Y%m%d_%H%M%S").log


# Helper functions to declutter docker exec call

# docker_exec: 
#	calls morph-xr2rml container tool to transform MongoDB collection into RDF representation according to a template
# arguments:
#	$1 - log output string
#	$2 - xr2rml template (*.ttl) file name
#	$3 - xr2rml output (*.ttl) file name
#	$4 - MongoDB collection name
docker_exec() {
	echo $1
	docker exec -w $WDIR $CONTAINER \
   		/bin/bash ./run_xr2rml_template.sh $TDIR/$2 $ODIR/$3 $DB $4 $DS $NS 
}

# docker_exec_multipart:
#	the same as docke_exec but splits a collection into 3 parts title, abstract, body_text to split the output
docker_exec_multipart() {
	echo $1

	docker exec -w $WDIR $CONTAINER \
   		/bin/bash ./run_xr2rml_template.sh $TDIR/$2 $ODIR/${3/part/title} $DB $4 $DS $NS title

	docker exec -w $WDIR $CONTAINER \
   		/bin/bash ./run_xr2rml_template.sh $TDIR/$2 $ODIR/${3/part/abstract} $DB $4 $DS $NS abstract

	docker exec -w $WDIR $CONTAINER \
   		/bin/bash ./run_xr2rml_template.sh $TDIR/$2 $ODIR/${3/part/body_text} $DB $4 $DS $NS body_text
}

# Check if the Docker container is running
if [ $( docker ps -f name=$CONTAINER| wc -l ) -eq 1 ]; then 
	echo "$CONTAINER container is not running. Restarting ..." >> $log 2>&1
	pushd $MORPH_XR2RML_DOCKER_COMPOSE_DIR
		docker-compose start
     	sleep 5s
	popd
fi


docker_exec "Generate documents' metadata..." \
            xr2rml_document_metadata.tpl.ttl \
            issa-document-metadata.ttl \
            document_metadata

docker_exec "Generate documents thematic descriptors by documentalists" \
            xr2rml_document_descriptors.tpl.ttl \
            issa-document-descriptors.ttl \
            document_descriptors

docker_exec "Generate documents' thematic descriptors by Annif" \
            xr2rml_annif_descriptors.tpl.ttl \
            issa-document-annif-descriptors.ttl \
            annif_descriptors

docker_exec "Generate domain descriptors by documentalists" \
            xr2rml_document_domains.tpl.ttl \
            issa-document-domains.ttl \
            document_domains

docker_exec "Generate keyword descriptors by authors" \
            xr2rml_document_keywords.tpl.ttl \
            issa-document-keywords.ttl \
            document_keywords

docker_exec "Generate documents' full-text RDF" \
            xr2rml_document_text.tpl.ttl \
            issa-document-text.ttl \
            document_text

docker_exec "Generate documents' Rao Stirling annotations" \
            xr2rml_rao_stirling_index.tpl.ttl \
            issa-document-rao-stirling.ttl \
            rao_stirling


docker_exec_multipart "Generate annotations for DBpedia Spotlight" \
                      xr2rml_spotlight_annot.tpl.ttl \
                      issa-document-spotlight-part.ttl \
                      spotlight_filtered 

docker_exec_multipart "Generate annotations for Entity-fishing" \
                      xr2rml_entityfishing_annot.tpl.ttl \
                      issa-document-entityfishing-part.ttl \
                      entityfishing_filtered 


docker_exec_multipart "Generate annotations for GeoNames" \
                      xr2rml_geonames_annot.tpl.ttl \
                      issa-document-geonames-part.ttl \
                      geonames_filtered 

############################################################################
## use-case specific annotations 
############################################################################

docker_exec_multipart "Generate annotations for Pyclinrec" \
     	               xr2rml_pyclinrec_annot.tpl.ttl \
          	           issa-document-pyclinrec-part.ttl \
               	       pyclinrec_filtered 
