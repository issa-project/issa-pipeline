#!/bin/bash
# Authors: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#        : Anna BOBASHEVA, University Cote d'Azur, Inria


# ISSA environment definitions
. ../../env.sh

echo "input database: $MONGODB_DB"
echo "output rdf dir: $XR2RML_OUTPUT_DIR"

# Directory where the output files are stored
mkdir -p $XR2RML_OUTPUT_DIR

# Change the Mongo database name in the xr2rml.properties for a current one
sed -i "/^database.name\[0\]=/s/=.*/=$MONGODB_DB/" xr2rml.properties

# Shorten var names for readability
DSN=$ISSA_DATASET_NAME
ODIR=$XR2RML_OUTPUT_DIR

echo "Generate articles metadata..."
./run_xr2rml.sh $DSN document_metadata xr2rml_document_metadata.tpl.ttl $ODIR/issa-document-metadata.ttl

echo "Generate articles thematic descriptors by documentalists"
./run_xr2rml.sh $DSN document_descriptors xr2rml_document_descriptors.tpl.ttl   $ODIR/issa-document-descriptors.ttl
 
echo "Generate articles' full text RDF"
./run_xr2rml.sh  $DSN article_text xr2rml_article_text.tpl.ttl  $ODIR/issa-article-text.ttl

echo  "Generate articles' thematic descriptors genearated by Annif"
./run_xr2rml.sh $DSN annif_descriptors  xr2rml_annif_descriptors.tpl.ttl   $ODIR/issa-article-annif-descriptors.ttl

echo  "Generate annotations for DBpedia Spotlight"
./run_xr2rml_annotation.sh $DSN title     spotlight xr2rml_spotlight_annot.tpl.ttl $ODIR/issa-article-spotlight-title.ttl
./run_xr2rml_annotation.sh $DSN abstract  spotlight xr2rml_spotlight_annot.tpl.ttl $ODIR/issa-article-spotlight-abstract.ttl
./run_xr2rml_annotation.sh $DSN body_text spotlight xr2rml_spotlight_annot.tpl.ttl $ODIR/issa-article-spotlight-body.ttl

echo "Generate annotations for Entity-fishing" 
./run_xr2rml_annotation.sh $DSN title     entityfishing xr2rml_entityfishing_annot.tpl.ttl $ODIR/issa-article-entityfishing-title.ttl
./run_xr2rml_annotation.sh $DSN abstract  entityfishing xr2rml_entityfishing_annot.tpl.ttl $ODIR/issa-article-entityfishing-abstract.ttl
./run_xr2rml_annotation.sh $DSN body_text entityfishing xr2rml_entityfishing_annot.tpl.ttl $ODIR/issa-article-entityfishing-body.ttl

echo "Generate annotations for GeoNames" 
./run_xr2rml_annotation.sh $DSN title     geonames xr2rml_geonames_annot.tpl.ttl $ODIR/issa-article-geonames-title.ttl
./run_xr2rml_annotation.sh $DSN abstract  geonames xr2rml_geonames_annot.tpl.ttl $ODIR/issa-article-geonames-abstract.ttl
./run_xr2rml_annotation.sh $DSN body_text geonames xr2rml_geonames_annot.tpl.ttl $ODIR/issa-article-geonames-body.ttl



# Generate annotations for Entity-fishing (body)
#collections=$(mongo $MONGODB_DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | egrep "entityfishing_._body")
#index=0
#for collection in $collections; do
#    echo "Processing collection $collection"
#    ./run_xr2rml_annotation_split.sh $DSN body_text $collection xr2rml_entityfishing_tpl.ttl 10000000 $ODIR/cord19-nekg-entityfishing-body.ttl.${index}
#    index=$(($index + 1))
#done

