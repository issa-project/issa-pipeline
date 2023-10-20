#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# 
# Run this script to restore ALL graph data in Virtuoso in case it was deleted or corrupted.
#
# $1 - the argument containing the name of the ISSA instance

export ISSA_INSTANCE=$1

# ISSA environment definitions
. ../../env.sh

echo "ISSA instance         : $ISSA_INSTANCE"
echo "graph namespace       : $ISSA_NAMESPACE"
echo "input host rdf dir    : $VIRTUOSO_HOST_DATA_DIR"
echo "import script dir     : $VIRTUOSO_CONT_SCRIPT_DIR"

echo "This script clears and reloads the entire dataset graph for ISSA instance  $ISSA_INSTANCE."
echo "Would you like to proceed? (y/n)"
read answer
if [[ ! "$answer" == [Yy]* ]]; then
	exit
fi

echo "************************************************************************"
echo " Uploading all ISSA generated RDF (Turtle) files to triplestore..."
echo "************************************************************************"

./run-recovery.sh

echo "************************************************************************"
echo " Uploading Geonames to triplestore..."
echo "************************************************************************"
	pushd $ISSA_ROOT/environment/datasets/agrovoc
	
		./import-geonames.sh

	popd 

echo "************************************************************************"
echo " Uploading DBPedia and Wikidata hierarchies to triplestore..."
echo "************************************************************************"
	pushd $ISSA_ROOT/environment/datasets/dbpedia
	
		./run-update.sh

	pushd $ISSA_ROOT/environment/datasets/wikidata
	
		./run-update.sh

	popd
	popd


echo "************************************************************************"
echo " Uploading instance specific datasets to triplestore..."
echo "************************************************************************"

if [[ $ISSA_INSTANCE == "agritrop" ]] ; then 
	echo "Agrovoc"

	pushd $ISSA_ROOT/environment/datasets/agrovoc
	
		./import-agrovoc.sh

	echo "AgrIST"

	pushd $ISSA_ROOT/environment/datasets/agrist
	
		./import-agrist.sh

	popd 
	popd 
fi

if [[ $ISSA_INSTANCE == "hal" ]] ; then 
	echo "HAL Domains"

	pushd $ISSA_ROOT/environment/datasets/hal-domains
	
		./import-hal-domains.sh

	echo "MeSH"

	pushd $ISSA_ROOT/environment/datasets/mesh
	
		./import-mesh.sh

	popd 
	popd 

fi

