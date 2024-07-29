# OpenAlex topics hierarchy


Retrieve the hierarchy of [topics in OpenAlex](https://docs.openalex.org/api-entities/topics).
This consists of 4 levels: domains, fields, subfields, topics.

Each domain, field, subfield and topic is represented in RDF using the SPARQL micro-service [openalex/getTopicsHierarchy](../../sparql-micro-services/openalex/getTopicsHierarchy).

Script `run.sh` will invoke the SPARQL micro-service, store the result in `openalex-topics-dump.ttl`, then load the result into Virtuoso as named graph `<http://data-issa.cirad.fr/graph/openalex-topics-hierarchy>`.
