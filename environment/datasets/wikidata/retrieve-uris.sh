#!/bin/bash
# Query all unique URIs from the annotations generated by entity-fishing

# Set the number of URIs to retrieve
#size=56987

query=$(cat << EOF
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oa: <http://www.w3.org/ns/oa#>
SELECT (count(distinct ?uri) as ?cnt)
FROM <http://data-issa.cirad.fr/graph/entity-fishing-nes>
FROM <http://data-issa.cirad.fr/graph/wikidata-named-entities>
WHERE { ?annot oa:hasBody ?uri. 
        FILTER NOT EXISTS {GRAPH <http://data-issa.cirad.fr/graph/wikidata-named-entities> {?uri rdfs:label ?wdLabel .}}}
EOF
)

size=$(curl -H "accept: text/csv" \
            --data-urlencode "query=${query}" \
     	    http://localhost:8890/sparql \
			| grep -o -E '[0-9]+' )



# Max number of URIs to retrieve at once (limit of the SPARQL endpoint)
limit=10000

query=$(cat << EOF
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX oa: <http://www.w3.org/ns/oa#>
SELECT DISTINCT ?uri
FROM <http://data-issa.cirad.fr/graph/entity-fishing-nes>
FROM <http://data-issa.cirad.fr/graph/wikidata-named-entities>
WHERE { ?annot oa:hasBody ?uri. 
        FILTER NOT EXISTS {GRAPH <http://data-issa.cirad.fr/graph/wikidata-named-entities> {?uri rdfs:label ?wdLabel .}}}
LIMIT ${limit}
OFFSET 

EOF
)
 
result=wikidata-ne-uris.txt

resulttmp=/tmp/sparql-response-$$.ttl
echo -n "" > $resulttmp

offset=0

while [ "$offset" -lt "$size" ]
do
    echo "Retrieving URIs starting at $offset..."

    echo "${query}${offset}"

    curl -H "accept: text/csv" \
		--data-urlencode "query=${query}${offset}" \
     	http://localhost:8890/sparql \
        | grep -v '"uri"' | sed 's|"||g' >> $resulttmp
     offset=$(($offset + $limit))
     
done

cat $resulttmp | sort | uniq > $result
rm $resulttmp

