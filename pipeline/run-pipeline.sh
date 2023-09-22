#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Integration of ISSA pipeline steps 

export PIPELINE_INSTANCE=$1

# ISSA environment definitions
. ../env.sh

echo "$ISSA_INSTANCE"
echo "$ISSA_DATASET"
echo "$LATEST_UPDATE"


echo "Downloading metadata..."
./1_load_metadata.sh
echo "    done"

echo "Downloading and extraction article text..."
./2_extract_pdf_text.sh
echo "    done"

echo "Indexing with thematic descriptors..."
./3_index_articles.sh
echo "    done"

echo "Annotating with named entities..."
./4_annotate_articles.sh
"    done"

echo "Transforming to RDF..."
./5_transform_to_rdf.sh
echo "    done"

echo "Uploading to triple store..."
./6_upload_to_triplestore.sh
echo "    done"

