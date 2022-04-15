#!/bin/bash
# Authors: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#        : Anna BOBASHEVA, University Cote d'Azur, Inria


# ISSA environment definitions
. ../../env.sh

# Directory where the output files are stored
ODIR=$XR2RML_OUTPUT_DIR
DB=$MONGODB_DB

echo "input database: $DB"
echo "output rdf dir: $ODIR"

mkdir -p $ODIR

echo "Generate articles metadata..."
./run_xr2rml.sh $DB document_metadata agritrop_id xr2rml_document_metadata_tpl.ttl $ODIR/issa-document-metadata.ttl

echo "Generate articles thematic descriptors by documentalists"
./run_xr2rml.sh $DB document_descriptors agritrop_id xr2rml_document_descriptors_tpl.ttl   $ODIR/issa-document-descriptors.ttl
 
echo "Generate articles' full text RDF"
./run_xr2rml.sh  $DB article_text paper_id xr2rml_article_text_tpl.ttl  $ODIR/issa-article-text.ttl

echo  "Generate articles' thematic descriptors genearated by Annif"
./run_xr2rml.sh $DB annif_descriptors paper_id  xr2rml_annif_descriptors_tpl.ttl   $ODIR/issa-article-annif-descriptors.ttl

echo  "Generate annotations for DBpedia Spotlight"
./run_xr2rml_annotation.sh $DB title     spotlight xr2rml_spotlight_nes_tpl.ttl $ODIR/issa-article-spotlight-title.ttl
./run_xr2rml_annotation.sh $DB abstract  spotlight xr2rml_spotlight_nes_tpl.ttl $ODIR/issa-article-spotlight-abstract.ttl
./run_xr2rml_annotation.sh $DB body_text spotlight xr2rml_spotlight_nes_tpl.ttl $ODIR/issa-article-spotlight-body.ttl

echo "Generate annotations for Entity-fishing" 
./run_xr2rml_annotation.sh $DB title     entityfishing xr2rml_entityfishing_nes_tpl.ttl $ODIR/issa-article-entityfishing-title.ttl
./run_xr2rml_annotation.sh $DB abstract  entityfishing xr2rml_entityfishing_nes_tpl.ttl $ODIR/issa-article-entityfishing-abstract.ttl
./run_xr2rml_annotation.sh $DB body_text entityfishing xr2rml_entityfishing_nes_tpl.ttl $ODIR/issa-article-entityfishing-body.ttl

echo "Generate annotations for GeoNames" 
./run_xr2rml_annotation.sh $DB title     geonames xr2rml_geonames_nes_tpl.ttl $ODIR/issa-article-geonames-title.ttl
./run_xr2rml_annotation.sh $DB abstract  geonames xr2rml_geonames_nes_tpl.ttl $ODIR/issa-article-geonames-abstract.ttl
./run_xr2rml_annotation.sh $DB body_text geonames xr2rml_geonames_nes_tpl.ttl $ODIR/issa-article-geonames-body.ttl



# Generate annotations for Entity-fishing (body)
#collections=$(mongo $DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | egrep "entityfishing_._body")
#index=0
#for collection in $collections; do
#    echo "Processing collection $collection"
#    ./run_xr2rml_annotation_split.sh $DB body_text $collection xr2rml_entityfishing_tpl.ttl 10000000 $ODIR/cord19-nekg-entityfishing-body.ttl.${index}
#    index=$(($index + 1))
#done

