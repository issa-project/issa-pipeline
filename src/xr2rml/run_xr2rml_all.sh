#!/bin/bash
# Authors: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#        : Anna BOBASHEVA, University Cote d'Azur, Inria


# ISSA environment definitions
. ../env.sh

for LANG in en fr; do

    # Directory where the output files are stored
    ODIR=$ISSA_DATA_ROOT/$ISSA_DATASET/$LANG/$ISSA_RDF
    mkdir -p $ODIR

    # Generate articles metadata
    #./run_xr2rml_metadata.sh $DB metadata_$LANG agritrop_id   xr2rml_metadata_issa_tpl.ttl   $ODIR/issa-articles-metadata_${LANG}.ttl


    # Generate articles full text RDF
    ./run_xr2rml_fulltext.sh  $DB  fulltext_$LANG paper_id xr2rml_fulltext_issa_tpl.ttl  $ODIR/issa-articles-fulltext_${LANG}.ttl


    # Generate annotations for DBpedia Spotlight
    #./run_xr2rml_annotation.sh $DB title     spotlight_$LANG xr2rml_spotlight_tpl.ttl $ODIR/issa-articles-spotlight-title_${LANG}.ttl
    #./run_xr2rml_annotation.sh $DB abstract  spotlight_$LANG xr2rml_spotlight_tpl.ttl $ODIR/issa-articles-spotlight-abstract_${LANG}.ttl
    #./run_xr2rml_annotation.sh $DB body_text spotlight_$LANG xr2rml_spotlight_tpl.ttl $ODIR/issa-articles-spotlight-body_${LANG}.ttl

    # Generate annotations for Entity-fishing 
    #./run_xr2rml_annotation.sh $DB title     entityfishing_$LANG xr2rml_entityfishing_tpl.ttl $ODIR/issa-articles-entityfishing-title_${LANG}.ttl
    #./run_xr2rml_annotation.sh $DB abstract  entityfishing_$LANG xr2rml_entityfishing_tpl.ttl $ODIR/issa-articles-entityfishing-abstract_${LANG}.ttl
    #./run_xr2rml_annotation.sh $DB body_text entityfishing_$LANG xr2rml_entityfishing_tpl.ttl $ODIR/issa-articles-entityfishing-body_${LANG}.ttl

    # Generate annotations for Geographic entities
    #./run_xr2rml_annotation.sh $DB abstract geographic_entities xr2rml_geographic_entities_tpl.ttl $ODIR/geographic_entities_abstract.ttl

done


# Generate annotations for Entity-fishing (body)
#collections=$(mongo $DB --eval "db.getCollectionNames()" | cut -d'"' -f2 | egrep "entityfishing_._body")
#index=0
#for collection in $collections; do
#    echo "Processing collection $collection"
#    ./run_xr2rml_annotation_split.sh $DB body_text $collection xr2rml_entityfishing_tpl.ttl 10000000 $ODIR/cord19-nekg-entityfishing-body.ttl.${index}
#    index=$(($index + 1))
#done

