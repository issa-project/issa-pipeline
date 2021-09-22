#!/bin/bash
# Author: Franck MICHEL, University Cote d'Azur, CNRS, Inria

# Environment definitions
. ../env.sh

# Directory where the output files are stored (relative to the current directory)
ODIR=./$DATASET_ID
mkdir -p $ODIR


# Generate annotations for entity-fishing
./run_xr2rml_annotation.sh $DATASET_ID abstract geographic_entities xr2rml_geographic_entities_tpl.ttl $ODIR/geographic_entities_abstract.ttl
