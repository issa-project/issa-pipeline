# Load OpenAlex data


Script `run.sh` loads into Virtuoso the annotations of articles wrt.:
  - the Sustainable Development goals (SDGs), 
  - the OpenAlex topics that include annotations about the whole hierarchy (domains, fields, subfields, topics), 
  - the OpenAlex authorships that include the authors and their institutions

Before running the script, store the input files in this folder.


| Input file | SPARQL micro-service to use <br>to generate the input file | Target named graph |
|-|-|-|
| `openalex-sdgs.ttl` | [openalex/getSdgsByDoi](../../sparql-micro-services/openalex/getSdgsByDoi) | `http://data-issa.cirad.fr/graph/openalex-sdgs` |
| `openalex-topics.ttl` | [openalex/getTopicsByDoi](../../sparql-micro-services/openalex/getTopicsByDoi) | `http://data-issa.cirad.fr/graph/openalex-topics` |
| `openalex-authorships.ttl` | [openalex/getAuthorshipsByDoi](../../sparql-micro-services/openalex/getAuthorshipsByDoi) | `http://data-issa.cirad.fr/graph/openalex-authorships` |
