# External Datasets 

In addition to the ISSA pipeline generated data other RDF datasets can be loaded into the same triple store. Especially ot makes sense to load the external datasets containing the entities that are referenced by the ISSA data, such as GeoNames, Wikidata or DBpedia. The dataset might also contain the related entities that allow for more elaborate reasoning on the ISSA knowledge graph.

Each external dataset is and open source dataset and  has a unique process of obtaining and loading the data as well as a specific update schedule.

## Common datasets

Three datasets, GeoNames, Wikidata and DBpedia, are referred to by the Named Entities recognized by the NER processing of the document corpus and would be common for all use cases (instances) of ISSA.

- [GeoNames](https://www.geonames.org) is a large database of geographical entities. It is not updated often and we recommend loading it once. See GeoNames ontology [documentation](https://www.geonames.org/ontology/documentation.html).
 
- [Wikidata](https://www.wikidata.org/) is a free and open knowledge base that can be read and edited by both humans and machines. It is not possible to store it locally due to its size and frequent updates. Therefore we periodically extract and store the entities that are already referenced and their hierarchical relationships.

- [DBpedia](https://www.dbpedia.org/) is a project aiming to extract structured content from the information created in the Wikipedia. For the same reason it's quite unreasonable to store the entire datasets and we periodically extract and store only referenced entities and their hierarchical relationships.

## Instance-specific datasets 

In addition, each instance of the ISSA knowlege graph can be complemented with relevant external datasets.

#### Agritrop

- [Agrovoc](https://www.fao.org/agrovoc/) is a Linked Open Data set about agriculture available for public use. This dataset is in the core of the Agritrop thematic indexing and provides thematic descriptors' labels and relations in the form of a SKOS thesaurus. Agritrop is updated approximately once a month. See Agrovoc Linked Data [documentation](https://www.fao.org/agrovoc/index.php/linked-data).

- [agrist](https://agrist.cirad.fr/) is a vocabulary of agricultural science domains. These domains are referenced in the ISSA document's metadata for the instance of Agritrop.
  
#### HAL 

- [HAl domains](https://aurehal.archives-ouvertes.fr/domain?locale=en) ia a vocabulary of scientific domains that are referenced in document's metadata. This vocabulary is reconstructed from the graph in the HAL repository.
- [MeSH](https://www.nlm.nih.gov/mesh/meshhome.html) is the vocabulary thesaurus used for indexing articles for PubMed. Some of the HAL documents are indexed with MeSH descriptors. MeSH is updated  once a year. See more in the MeSH data [documentation](https://www.nlm.nih.gov/databases/download/mesh.html).
