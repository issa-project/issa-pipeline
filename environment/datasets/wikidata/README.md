This folder provides the scripts and queries used to retrieve all the Wikidata entities used as named entities in the ISSA knowledge graph.

The entities are dumped with their main label (`rdfs:label`) and alt labels (`skos:altLabel`).

Wikidata properties `wdt:P31` and `wdt:P279` are turned into their RDF/RDFS equivalent: `rdf:type` and `rdfs:subClassOf`. Property `wdt:P171`, which is used in life science to link a taxon to its parent, is also turned into `rdfs:subClassOf`.

`query-hierarchy.sparql` adds all the inferred `rdf:type` and `rdfs:subClassOf` properties. Typically, for the following pattern:
```turtle
  <a> wdt:P31 <B>. <B> wdt:P279 <C>. <C> wdt:P279 <D>.
```
this will generate:
```turtle
  <a> rdf:type <B>, <C>, <D>.
  <B> rdfs:subClassOf <C>, <D>.
  <C> rdfs:subClassOf <D>.
```
