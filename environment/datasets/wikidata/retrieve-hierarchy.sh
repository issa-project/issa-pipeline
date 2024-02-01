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

# Init log
log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/wikidata_dump_$lang-$(date "+%Y%m%d_%H%M%S").log

sparql_query=retrieve-hierarchy.sparql

# List of URIs to query
urilist=wikidata-ne-uris.txt

# Max number of URIs to query at once
MAXURIS=5

# Initialize the result file with the prefixes
cp namespaces.ttl $result_file
result_tmp=/tmp/sparql-response-$$.ttl

# SPARQL query pattern
fullquery_pattern=$(cat $sparql_query)
fullquery_pattern=${fullquery_pattern//\{\{lang\}\}/$lang}


# SPARQL parttern for one URI
subquery_pattern='
  { 
    {   # When uri is an instance of (P31) a class
        BIND(iri("{{uri}}") as ?uri)
        ?uri wdt:P31 ?uriClass.
        OPTIONAL { ?uriClass   (wdt:P279|wdt:P361)+   ?uriAnyParent. }
    }
    UNION
    {   # When uri is a subclass of (P279) a class or a part of (P361) another entity
        BIND(iri("{{uri}}") as ?uriClass)
        ?uriClass   (wdt:P279|wdt:P361)+   ?uriAnyParent.
    }
    UNION
    {   # When uri is a taxon
        BIND(iri("{{uri}}") as ?uriClass)
        ?uriClass   wdt:P171+   ?uriAnyParent.
    }
  }
'

# Split the list of URIs into multiple files of $MAXURIS URIs
uri_split=/tmp/uri_list-$$-
split -d -l $MAXURIS $urilist $uri_split

# Loop on all files of URIs
nbfiles=$(ls -l ${uri_split}* | wc -l)
nbfiles=$(($nbfiles - 1))
_fileIndex=0

for _uri_file_list in `ls ${uri_split}*`; do
    echo "--- Processing file $_uri_file_list (${_fileIndex}/$nbfiles)" >>$log

    # Create the pattern of the SPARQL query by adding one 
    _subquery='  {}'
    for _uri in `cat $_uri_file_list`; do
        # Add the subquery once for each URI
        _subquery="$_subquery UNION ${subquery_pattern//\{\{uri\}\}/$_uri}"
    done
    
    _fileIndex=$(($_fileIndex + 1))

    curl -o $result_tmp \
         -X POST \
         -H 'Accept: text/turtle' \
         -H "Content-Type: application/sparql-query" \
         --fail \
         --retry 10 \
         --silent --show-error \
         --w "    received %{size_download} bytes in %{time_total} sec; HTTP code: %{response_code}\n" \
         -d "${fullquery_pattern/\{\{pattern\}\}/$_subquery}" \
         https://query.wikidata.org/sparql                          >>$log

    # Check for errors and output failed uris
    res="$?"
    if [ $res -ne 0  ]; then
        echo "ERROR: $res.   Affected IRIs:"                        >>$log
        echo $(cat $_uri_file_list)                                 >>$log
        echo ""                                                     >>$log
        echo $(cat $result_tmp)                                     >>$log
        #empty temp file 
        > $result_tmp
    fi

    rm -f $_uri_file_list

    # Filter out "@prefix" lines
    cat $result_tmp | grep -v '^@' >> $result_file
    echo "# -----" >> $result_file

done
rm -f $result_tmp

