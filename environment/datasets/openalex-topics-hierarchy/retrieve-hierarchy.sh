#!/bin/bash
# Authors: Franck MICHEL, University Cote d'Azur, CNRS, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Query the SPARQL micro-service to retrieve the hierarchy of OpenAlex topics (https://docs.openalex.org/api-entities/topics).
# The SPARQL micro-service returns 200 results at a time (limit of the OpenAlex API), 
# so it must be invokved for as many pages as necessary.
#
# Parameters:
#   $1: output file name


# ISSA environment definitions
. ../../../env.sh

# Read input parameters
result_file=$1

# Number of results at each invokation (max page size)
per_page=200


# Init log file
log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/openalex-topics-$(date "+%Y%m%d_%H%M%S").log
echo "**** Starting $(date "+%Y-%m-%d %H:%M:%S")" >> $log

# Initialize the result file with the prefixes
cp namespaces.ttl $result_file
result_tmp=/tmp/sparql-response-$$.ttl


# Compute the number of pages to retrieve
curl -H "Accept: application/json" \
     -o $result_tmp \
     -X GET "https://api.openalex.org/topics?per-page=1&page=1"
total=$(jq 'getpath(["meta","count"])' $result_tmp) 
pages=$(($total / $per_page + 1))
echo "Will retrieve $total topics with $pages invocations" >> $log
rm -f $result_tmp


# SPARQL query to submit to the SPARQL micro-service
#prefix dct:    <http://purl.org/dc/elements/1.1/>
#prefix skos: <http://www.w3.org/2004/02/skos/core#>
#construct where { ?s ?p ?o. }
query='prefix%20dct%3A%20%20%20%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0Aprefix%20skos%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0Aconstruct%20where%20%7B%20%3Fs%20%3Fp%20%3Fo.%20%7D'

# SPARQL µservice URL
query_url="http://localhost/service/openalex/getTopicsHierarchy?query=$query&per_page=$per_page&page="


# Loop on all pages
for (( _page = 1; _page <= $pages; _page += 1 )); do
    echo "--- Processing page $_page/$pages" >> $log

    # Add page number to the SPARQL µservice URL
    _query="$query_url$_page"

    curl -o $result_tmp \
         -X GET \
         -H 'Accept: text/turtle' \
         --fail --retry 5 --silent --show-error \
         --w "    received %{size_download} bytes in %{time_total} sec; HTTP code: %{response_code}\n" \
         "$_query" >> $log

    # Check for errors
    res="$?"
    if [ $res -ne 0 ]; then
        echo "ERROR: $res, page: $_page, url: $_query:" >> $log
        # Empty temp file 
        echo > $result_tmp
    fi
    
    # Filter out "@prefix" lines
    cat $result_tmp | grep -v '^@' >> $result_file
    echo "# -----" >> $result_file

done
rm -f $result_tmp

echo "**** Finished $(date "+%Y-%m-%d %H:%M:%S")" >> $log
