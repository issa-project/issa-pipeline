#!/bin/bash
# Query DBpedia for each of the URIs to retrieve the hierarchy of classes of each URI.

# Script takes one parameter for language, default is en, no quotation marks
lang=${1:-en}

# Define log file
log_dir=../../logs
mkdir -p $log_dir 
log=$log_dir/dbpedia_dump_$lang-$(date "+%Y%m%d_%H%M%S").log

# List of URIs to query
urilist=dbpedia-ne-uris.txt

# Max number of URIs to query at once
MAXURIS=50

# Initialize the result file with the prefixes
result_file=dbpedia-dump-$lang.ttl
cp namespaces.ttl $result_file
result_tmp=/tmp/sparql-response-$$.ttl


# SPARQL query pattern, substitute the language
query_pattern=`cat query-hierarchy.sparql`
query_pattern=${query_pattern//\{\{lang\}\}/$lang}

# Split the list of URIs into multiple files of $MAXURIS URIs
urilist_split=/tmp/urilist-$$-
split -d -l $MAXURIS $urilist $urilist_split


# Loop on all files of URIs
nbfiles=$(ls -l ${urilist_split}* | wc -l)
nbfiles=$(($nbfiles - 1))
_fileIndex=0
#mkdir -p dumps

for _uri_file_list in `ls ${urilist_split}*`; do
    _fileIndex=$(($_fileIndex + 1))
    echo "" >>$log
    echo "--- Processing file $_uri_file_list (${_fileIndex}/$nbfiles)"	>>$log

    # Create the list of URIs to embed in the SPARQL query
    _uri_list=''
    for _uri in `cat $_uri_file_list`; do
        _uri_list="$_uri_list <${_uri}>"
    done
    # Add commas between URIs: replace each "> <" by ">, <"
    _uri_list="${_uri_list//> </>, <}"
	


    curl -o $result_tmp \
         -X POST \
         -H 'Accept: text/turtle' \
         -S \
         -H "Content-Type: application/sparql-query" \
         -d "${query_pattern/\{\{uri_list\}\}/$_uri_list}" \
         https://dbpedia.org/sparql										2>>$log

    # Check for errors and output failed uris
    res="$?"
	if [ $res -ne 0  ]; then
    		echo $(cat $_uri_file_list)                            		         >>$log
	fi

    rm -f $_uri_file_list
	
	# Filter out "@prefix" lines
    cat $result_tmp | grep -v '^@' >> $result_file
    echo "# -----" >> $result_file

done

rm -f $result_tmp

