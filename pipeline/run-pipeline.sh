#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# Integration of ISSA pipeline steps 

echo "Downloading metadata..."
./1_load_metadata.sh
"    done"

echo "Downloading and extraction article text..."
./2_extract_articles_text.sh
"    done"

echo "Indexing with thematic descriptors..."
./3_index_articles.sh
"    done"

echo "Annotating with named entities..."
./4_annotate_articles.sh
"    done"

echo "Transforming to RDF..."
./5_transform_to_rdf.sh
"    done"

echo "Uploading to triple store..."
./6_upload_to_triplestore.sh
"    done"

