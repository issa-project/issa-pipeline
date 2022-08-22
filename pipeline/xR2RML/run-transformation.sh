#!/bin/bash
# Authors: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#        : Anna BOBASHEVA, University Cote d'Azur, Inria


# ISSA environment definitions
. ../../env.sh


# Shorten var names for readability
DB=$MONGODB_DB
DS=$ISSA_DATASET_NAME
ODIR=$XR2RML_OUTPUT_DIR

echo "input database: $DB"
echo "output rdf dir: $ODIR"

# Directory where the output files are stored
mkdir -p $ODIR

# Change the Mongo database name in the xr2rml.properties for a current one
sed -i "/^database.name\[0\]=/s/=.*/=$DB/" xr2rml.properties


echo "Generate articles metadata..."
./run_xr2rml.sh $DS document_metadata xr2rml_document_metadata.tpl.ttl $ODIR/issa-document-metadata.ttl

echo "Generate articles thematic descriptors by documentalists"
./run_xr2rml.sh $DS document_descriptors xr2rml_document_descriptors.tpl.ttl   $ODIR/issa-document-descriptors.ttl
 
echo "Generate articles' full text RDF"
./run_xr2rml.sh  $DS article_text xr2rml_article_text.tpl.ttl  $ODIR/issa-article-text.ttl

echo  "Generate articles' thematic descriptors genearated by Annif"
./run_xr2rml.sh $DS annif_descriptors  xr2rml_annif_descriptors.tpl.ttl   $ODIR/issa-article-annif-descriptors.ttl

echo  "Generate annotations for DBpedia Spotlight"
./run_xr2rml_annotation.sh $DS title     spotlight_filtered xr2rml_spotlight_annot.tpl.ttl $ODIR/issa-article-spotlight-title.ttl
./run_xr2rml_annotation.sh $DS abstract  spotlight_filtered xr2rml_spotlight_annot.tpl.ttl $ODIR/issa-article-spotlight-abstract.ttl
./run_xr2rml_annotation.sh $DS body_text spotlight_filtered xr2rml_spotlight_annot.tpl.ttl $ODIR/issa-article-spotlight-body.ttl

echo "Generate annotations for Entity-fishing" 
./run_xr2rml_annotation.sh $DS title     entityfishing_filtered xr2rml_entityfishing_annot.tpl.ttl $ODIR/issa-article-entityfishing-title.ttl
./run_xr2rml_annotation.sh $DS abstract  entityfishing_filtered xr2rml_entityfishing_annot.tpl.ttl $ODIR/issa-article-entityfishing-abstract.ttl
./run_xr2rml_annotation.sh $DS body_text entityfishing_filtered xr2rml_entityfishing_annot.tpl.ttl $ODIR/issa-article-entityfishing-body.ttl

echo "Generate annotations for GeoNames" 
./run_xr2rml_annotation.sh $DS title     geonames xr2rml_geonames_annot.tpl.ttl $ODIR/issa-article-geonames-title.ttl
./run_xr2rml_annotation.sh $DS abstract  geonames xr2rml_geonames_annot.tpl.ttl $ODIR/issa-article-geonames-abstract.ttl
./run_xr2rml_annotation.sh $DS body_text geonames xr2rml_geonames_annot.tpl.ttl $ODIR/issa-article-geonames-body.ttl

echo "Generate annotations for Agrovoc Pyclinrec" 
./run_xr2rml_annotation.sh $DS title     pyclinrec xr2rml_pyclinrec_annot.tpl.ttl $ODIR/issa-article-pyclinrec-title.ttl
./run_xr2rml_annotation.sh $DS abstract  pyclinrec xr2rml_pyclinrec_annot.tpl.ttl $ODIR/issa-article-pyclinrec-abstract.ttl
./run_xr2rml_annotation.sh $DS body_text pyclinrec xr2rml_pyclinrec_annot.tpl.ttl $ODIR/issa-article-pyclinrec-body.ttl


# Generate annotations for Entity-fishing (body)
#collections=$(mongo $MONGODB_DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | egrep "entityfishing_._body")
#index=0
#for collection in $collections; do
#    echo "Processing collection $collection"
#    ./run_xr2rml_annotation_split.sh $DS body_text $collection xr2rml_entityfishing_tpl.ttl 10000000 $ODIR/cord19-nekg-entityfishing-body.ttl.${index}
#    index=$(($index + 1))
#done

