#!/bin/bash
# Query DBpedia for each of the URIs to retrieve the hierarchy of classes of each URI.

# Script takes one parameter for language, default is en, no quotation marks
lang=${1:-en}

# Define namespace for the resources and dbpedia instance for the language 
if [ $lang == "en" ]; then
	ns=http://dbpedia.org/
     endpoint=https://dbpedia.org/sparql
elif [ $lang == "fr" ]; then
	ns=http://fr.dbpedia.org/
     endpoint=https://fr.dbpedia.org/sparql
fi

# Define log file
log_dir=../../logs
mkdir -p $log_dir 
log=$log_dir/dbpedia_dump_$lang-$(date "+%Y%m%d_%H%M%S").log

# List of URIs to query
urilist=dbpedia-ne-uris.txt

# Max number of URIs to query at once
MAXURIS=50

# Extract URIs for the requested language  
cat $urilist | grep "^${ns}" > dbpedia-ne-uris-$lang.txt
urilist=dbpedia-ne-uris-$lang.txt

# Split the list of URIs into multiple files of $MAXURIS URIs
urilist_split=/tmp/urilist-$$-
split -d -l $MAXURIS $urilist $urilist_split

# SPARQL query pattern, substitute the language
query_pattern=`cat query-hierarchy.sparql`
query_pattern=${query_pattern//\{\{lang\}\}/$lang}


# Initialize the result file with the prefixes
result_file=dbpedia-dump-$lang.ttl
cp namespaces.ttl $result_file
result_tmp=/tmp/sparql-response-$$.ttl


# Loop on all files of URIs
nbfiles=$(ls -l ${urilist_split}* | wc -l)
nbfiles=$(($nbfiles - 1))
_fileIndex=0

for _uri_file_list in `ls ${urilist_split}*`; do
    echo "--- Processing file $_uri_file_list (${_fileIndex}/$nbfiles)"	>>$log

    # Create the list of URIs to embed in the SPARQL query
    _uri_list=''
    for _uri in `cat $_uri_file_list`; do
        _uri_list="$_uri_list <${_uri}>"
    done

    # Add commas between URIs: replace each "> <" by ">, <"
    _uri_list="${_uri_list//> </>, <}"
	
    _fileIndex=$(($_fileIndex + 1))

    curl -o $result_tmp \
         -X POST \
         -H 'Accept: text/turtle' \
         -H "Content-Type: application/sparql-query" \
         --fail \
         --retry 10 \
	    --silent --show-error \
         --w "    received %{size_download} bytes in %{time_total} sec; HTTP code: %{response_code}\n" \
         -d "${query_pattern/\{\{uri_list\}\}/$_uri_list}" \
         $endpoint								                    >>$log

    # Check for errors and output failed uris
    res="$?"
	if [ $res -ne 0  ]; then
         echo "ERROR: $res.   Affected IRIs:" 						>>$log
    	    echo $(cat $_uri_file_list) 								>>$log
         echo ""												>>$log
         echo $(cat $result_tmp) 									>>$log
         #empty temp file 
         > $result_tmp
	fi

    rm -f $_uri_file_list
	
    # Filter out "@prefix" lines but not those that begin with 'ns'
    cat $result_tmp | grep '^@prefix ns' >> $result_file
    cat $result_tmp | grep -v '^@' >> $result_file
    echo "# -----" >> $result_file

done

rm -f $result_tmp

