# OpenAlex topics hierarchy


Retrieve the hierarchy of [topics in OpenAlex](https://docs.openalex.org/api-entities/topics); that consists of 4 levels: domains, fields, subfields, topics.
This information is stored as a reference mainly to get the labels. 
The tool should be invoked once in a while (e.g. monthly) or in case OpenAlex changes the list of topics and their hierarchy (which is not likely to be frequent).

Each domain, field, subfield and topic is represented in RDF using the SPARQL micro-service [openalex/getTopicsHierarchy](../../sparql-micro-services/openalex/getTopicsHierarchy).

Script `run.sh` invokes the SPARQL micro-service, stores the result in `openalex-topics-dump.ttl`, then loads the result into Virtuoso as named graph `<http://data-issa.cirad.fr/graph/openalex-topics-hierarchy>`.
