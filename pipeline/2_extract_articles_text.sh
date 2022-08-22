#!/bin/bash
# Author: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
# ISSA create full text corpus

# ISSA environment definitions & export
. ../env.sh

echo "************************************************************************"
echo " Downloading PDFs and extracting text from them..."
echo "************************************************************************"

docker start grobid
sleep 5 

source ${ISSA_VENV}/bin/activate

pushd ./fulltext

	python3 ./extract_text_from_pdf.py
	python3 ./coalesce_meta_json.py


popd

deactivate

docker stop grobid
