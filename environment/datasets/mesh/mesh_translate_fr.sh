#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# The official MESH thesaurus dump doe not have french labels. As a workaround, we use already 
# created mesh_en.tsv file and manully downloaded *fredesc2022.xml* from  from https://mesh.inserm.fr/FrenchMesh/
# with MeSH concepts in Englishenglish and French to create mesh_fr.tsv file for Pyclinrec annotations
# Run this script after craeting pyclinrec Docker container and mesh_en.tsv file

#TODO: craete a Turtle file instaed of tsv file

ISSA_INSTANCE=hal

# ISSA environment definitions
. ../../../env.sh


log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/mesh_translate_$(date "+%Y%m%d_%H%M%S").log

#activate python virtual environment
source $ISSA_VENV/bin/activate

# call Python script to transplate MeSH concepts into French
python3 -m translate_MeSH_into_French > $log

# deactivate python virtual environment
deactivate

# start Pyclinrec container
docker start pyclinrec
sleep 5

# send /add_annottator Http request to add Pyclinrec annotator
curl -X POST http://localhost:5002/add_annotator --data-urlencode "name=mesh" --data-urlencode "lang=fr" --data-urlencode "endpoint=None" --data-urlencode "graph=None" -H "Accept: application/json" >> $log

# stop Pyclinrec container
docker stop pyclinrec
