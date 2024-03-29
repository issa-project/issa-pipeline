#!/bin/bash
# Authors: Anna BOBASHEVA, University Cote d'Azur, Inria
#
# Licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
#
# Query Wikidata to retrieve the hierarchy of classes of each URI in file wikidata-ne-uris.txt

# ISSA environment definitions
. ../../../env.sh
# Script takes one parameter for language, default is en, no quotation marks


lang=${1:-en}

log_dir=${ISSA_ENV_LOG:-../../logs}
mkdir -p $log_dir 
log=$log_dir/wikidata_dump_$lang-$(date "+%Y%m%d_%H%M%S").log


# List of URIs to query
urilist=wikidata-ne-uris.txt

# Max number of URIs to query at once
MAXURIS=10

# Initialize the result file with the prefixes
result_file=wikidata-dump-$lang.ttl
cp namespaces.ttl $result_file
result_tmp=/tmp/sparql-response-$$.ttl

# SPARQL query pattern
fullquery_pattern=`cat query-hierarchy.sparql`
fullquery_pattern=${fullquery_pattern//\{\{lang\}\}/$lang}


# SPARQL parttern for one URI
subquery_pattern='
  { BIND(iri("{{uri}}") as ?uri)
    {?uri wdt:P279+ ?uriParent.}
    UNION
    {?uri wdt:P31/wdt:P279* ?uriClass.}
    UNION
    {?uri wdt:P171* ?uriParent.}
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
        _subquery="$_subquery UNION ${subquery_pattern/\{\{uri\}\}/$_uri}"
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
         https://query.wikidata.org/sparql                              >>$log

    # Check for errors and output failed uris
    res="$?"
	if [ $res -ne 0  ]; then
         echo "ERROR: $res.   Affected IRIs:" 						>>$log
    		echo $(cat $_uri_file_list) 								>>$log
         echo ""													>>$log
         echo $(cat $result_tmp) 									>>$log
         #empty temp file 
         > $result_tmp
	fi

    rm -f $_uri_file_list

    # Filter out "@prefix" lines
    cat $result_tmp | grep -v '^@' >> $result_file
    echo "# -----" >> $result_file

done
rm -f $result_tmp

