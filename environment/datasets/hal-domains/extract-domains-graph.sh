#!/bin/bash
# Query HAL to dump the subjects thesaurus

# Define log file
log_dir=../../logs
mkdir -p $log_dir 
log=$log_dir/hal_subjects_dump_-$(date "+%Y%m%d_%H%M%S").log


# Define the SPARQL query
query="
CONSTRUCT {
  ?s ?p ?o
}
WHERE {
  GRAPH <https://data.archives-ouvertes.fr/subject/> {
    ?s ?p ?o
  }
}"

# Construct the SPARQL endpoint URL
endpoint_url="http://sparql.archives-ouvertes.fr/sparql"

# Define output file
result_file=hal-domains-dump.ttl

# Make the SPARQL query request using curl with POST method
curl -X POST\
     -H "Content-Type: application/x-www-form-urlencoded"\
     -H 'Accept: text/turtle' \
     --data-urlencode "query=$query"\
     --fail --retry 10 \
	 --silent --show-error \
     --w "    received %{size_download} bytes in %{time_total} sec; HTTP code: %{response_code}\n" \
     -o $result_file\
     "$endpoint_url" >>$log # hal-subjects-dump.ttl

# Check for errors 
res="$?"
if [ $res -ne 0  ]; then
   echo "ERROR: $res" 	>>$log
fi


echo "Graph extracted and saved to $result_file"

