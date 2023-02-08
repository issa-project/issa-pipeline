#!/bin/bash
# Authors: Anna BOBASHEVA, University Cote d'Azur, Inria
#          Raphael Gazotti
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


# ISSA environment definitions
. ../../../env.sh

# Pull Docker image : no tagged version is abvailable for the DBPedia spotlight

docker pull dbpedia/dbpedia-spotlight:latest

# Load language models

for lang in $SPOTLIGHT_LANGUAGES; do
     lang_dir="$SPOTLIGHT_MODEL_DIR"/$lang

     if [ -d "$lang_dir" ]; then
		echo "$lang model is already loaded"         
		continue
	 fi
         
     mkdir -p "$lang_dir"

     query="PREFIX dataid: <http://dataid.dbpedia.org/ns/core#>
            PREFIX dataid-cv: <http://dataid.dbpedia.org/ns/cv#>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX dcat:  <http://www.w3.org/ns/dcat#>
	    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

            SELECT DISTINCT ?file WHERE {
               ?dataset dataid:artifact <https://databus.dbpedia.org/dbpedia/spotlight/spotlight-model> .
               ?dataset dcat:distribution ?distribution .
               {
                  ?distribution dct:hasVersion ?latestVersion
                  {
                        SELECT (?version as ?latestVersion) WHERE {
                                ?dataset dataid:artifact <https://databus.dbpedia.org/dbpedia/spotlight/spotlight-model> .
                                ?dataset dct:hasVersion ?version .
                        } ORDER BY DESC (?version) LIMIT 1
                  }
                  ?distribution dataid:contentVariant '$lang'^^xsd:string .
               }
               ?distribution dcat:downloadURL ?file .
            }"

      # get model URL

      result=`curl --data-urlencode query="$query" --data-urlencode format="text/tab-separated-values" https://databus.dbpedia.org/repo/sparql | sed 's/"//g' | grep -v "^file$" | head -n 1 `

      echo $result
      
      # download model
      curl -O  $result

      tar -C "$SPOTLIGHT_MODEL_DIR" -xvf spotlight-model_lang=$lang.tar.gz
      rm spotlight-model_lang=$lang.tar.gz
      echo "$lang model is downloaded "


done
