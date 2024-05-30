#!/bin/bash
# Authors: Anna BOBASHEVA & Franck MICHEL, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Query Wikidata to retrieve the hierarchy of instances classes of each URI in file wikidata-ne-uris.txt.
# The hierarchy involves properties P31 (rdf:type), subclass of (P279), part of (P361) and parent taxon (P171).
# In the result RDF, all properties are mapped to rdfs:subClassOf to make it easier to exploit afterwards.
#
# Parameters:
#   $1: output file name
#   $2: language, default is en, no quotation marks


# ISSA environment definitions
. ../../../env.sh

# Read input parameters
result_file=$1
lang=${2:-en}

# Max number of URIs to query at once
MAXURIS=2

# File containing the list of URIs to query
urilist=wikidata-ne-uris.txt


# Init log
log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/wikidata_dump_$lang-$(date "+%Y%m%d_%H%M%S").log
echo "**** Starting $(date "+%Y-%m-%d %H:%M:%S")" >> $log


# Initialize the result file with the prefixes
cp namespaces.ttl $result_file
result_tmp=/tmp/sparql-response-$$.ttl


# Template of the SPARQL query
fullquery_template=$(cat retrieve-hierarchy.sparql)
fullquery_template=${fullquery_template//\{\{lang\}\}/$lang}

# SPARQL query parttern for one URI
subquery_pattern=$(cat retrieve-hierarchy-pattern.sparql)


# Split the list of URIs into multiple files of $MAXURIS URIs
uri_split=/tmp/uri_list-$$-
split -d -l $MAXURIS $urilist $uri_split

# Loop on all files of URIs
nbfiles=$(ls -l ${uri_split}* | wc -l)
nbfiles=$(($nbfiles - 1))
_fileIndex=0

for _uri_file_list in `ls ${uri_split}*`; do
    echo "--- Processing file $_uri_file_list (${_fileIndex}/$nbfiles)" >> $log

    # Create the pattern of the SPARQL query by adding one 
    _subquery='  {}'
    for _uri in `cat $_uri_file_list`; do
        # Add the subquery once for each URI
        _subquery="$_subquery UNION ${subquery_pattern//\{\{uri\}\}/$_uri}"
    done
    final_query=${fullquery_template/\{\{pattern\}\}/$_subquery}

    _fileIndex=$(($_fileIndex + 1))

    curl -o $result_tmp \
         -X POST \
         -H 'Accept: text/turtle' \
         -H "Content-Type: application/sparql-query" \
         --fail \
         --retry 10 \
         --silent --show-error \
         --w "    received %{size_download} bytes in %{time_total} sec; HTTP code: %{response_code}\n" \
         -d "${final_query}" \
         https://query.wikidata.org/sparql                          >> $log

    # Check for network errors and output failed uris
    res="$?"
    if [ $res -ne 0 ]; then
        echo "ERROR: $res.   Affected IRIs:"                        >> $log
        cat $_uri_file_list                                         >> $log
        echo ""                                                     >> $log
        cat $result_tmp                                             >> $log
        # Empty temp file 
        echo > $result_tmp
    fi
    
    # Check for SPARQL timeout errors and output failed uris
    grep -q TimeoutException $result_tmp
    if [ $? -eq 0 ]; then
        echo "ERROR: TimeoutException.   Affected IRIs:"            >> $log
        cat $_uri_file_list                                         >> $log
        echo ""                                                     >> $log
        cat $result_tmp                                             >> $log
        # Empty temp file 
        echo > $result_tmp
    fi

    # Filter out "@prefix" lines
    cat $result_tmp | grep -v '^@' >> $result_file
    echo "# -----" >> $result_file
    rm -f $_uri_file_list

done
rm -f $result_tmp

echo "**** Finished $(date "+%Y-%m-%d %H:%M:%S")" >> $log
