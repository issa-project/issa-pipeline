# ISSA RDF data modeling

An article analyzed by the ISSA pipeline is described in three parts: general metadata (title, authors, publication date etc.), thematic descriptors characterizing the article, and named entities extracted from the article full-text.


## Namespaces
Below we use the following namespaces:

```turtle
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#>.
@prefix owl:    <http://www.w3.org/2002/07/owl#>.
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .

@prefix bibo:   <http://purl.org/ontology/bibo/> .
@prefix dce:    <http://purl.org/dc/elements/1.1/>.
@prefix dct:    <http://purl.org/dc/terms/>.
@prefix fabio:  <http://purl.org/spar/fabio/> .
@prefix eprint: <http://purl.org/eprint/type/> .
@prefix foaf:   <http://xmlns.com/foaf/0.1/>.
@prefix frbr:   <http://purl.org/vocab/frbr/core#>.
@prefix oa:     <http://www.w3.org/ns/oa#>.
@prefix prov:   <http://www.w3.org/ns/prov#>.
@prefix schema: <http://schema.org/>.

@prefix issa:   <http://data-issa.cirad.fr/>.
@prefix issapr: <http://data-issa.cirad.fr/property/>.
```

## Document metadata
Article URIs are formatted as http://data-issa.cirad.fr/article/article_id where article_id is a unique article identifier.

RDF resources representing documents can be instances of various classes depending in their type:
- conference article (`fabio:ConferencePaper`, `eprint:ConferencePaper`)
- journal article (`fabio:ResearchPaper`, `schema:ScholarlyArticle`, `bibo:AcademicArticle`, `eprint:JournalArticle`)
- book (`fabio:Book`, `eprint:Book`)
- book section (`fabio:BookChapter`, `eprint:BookItem`)
- thesis (`fabio:Thesis`, `eprint:Thesis`)
- application (`fabio:ComputerApplication`)
- data management plan (`fabio:DataManagementPlan`)
- film (`fabio:Film`)
- map (`bibo:Map`)
- monograph (`fabio:Expression`, `bibo:Document`)
- patent (`fabio:Patent`, `eprint:Patent`)

For each document, the available metadata are mapped as much as possible as follows (not all metadata exist for all types of documents):
- title (`dct:title`)
- authors (`dce:creator`)
- publication date (`dct:issued`)
- journal (`schema:publication`)
- license (`dct:license`)
- terms and conditions (`dct:rights`)
- identifiers
    - archive internal identifier (`dct:identifier`)
    - DOI (`bibo:doi`)
- source (API) from which the metadata information was retrieved (`dct:source`)
- article page URL (`schema:url`)
- source PDF download URL (`schema:downloadUrl`)
- alternate PDF download URLs (`schema:sameAs`)
- language
    - language string (`dce:language`)
    - language URI (`dct:language`)
- provenance
    - dataset name and version (`rdfs:isDefinedBy`)
    - source data URI (`prov:wasDerivedFrom`)
    - source data creation timestamp (`prov:generatedAtTime`), i.e. at which the article was added to the archive


Furthermore, articles are linked to their parts (title, abstract, body) as follows:
- `issapr:hasTitle <http://data-issa.cirad.fr/article/paper_id#title>`
- `dct:abstract   <http://data-issa.cirad.fr/article/paper_id#abstract>`
- `issapr:hasBody  <http://data-issa.cirad.fr/article/paper_id#body_text>`.
NOTE: only journal articles have associated body text 


Here is the example of journal article's metadata:
```turtle
<http://data-issa.cirad.fr/article/543654>
  a                      prov:Entity, fabio:ResearchPaper, bibo:AcademicArticle, eprint:JournalArticle, schema:ScholarlyArticle;
  dct:title              "Accounting for the ecological dimension in participatory research and development : lessons learned from Indonesia and Madagascar";
  dce:creator            "Pfund, Jean-Laurent", "Laumonier, Yves", "Bourgeois, Robin";
  schema:publication     "Ecology and Society";
  dct:issued             "2008.0"^^xsd:gYear;
  dct:rights             <https://agritrop.cirad.fr/mention_legale.html>;

  dct:source             "Agritrop-OAI2-API";
  dct:identifier         "543654";
  
  schema:url             <http://agritrop.cirad.fr/543654/> ;
  schema:downloadUrl     <http://agritrop.cirad.fr/543654/1/document_543654.pdf>;
  schema:sameAs          <http://www.ecologyandsociety.org/vol13/iss1/art15/>, <http://catalogue-bibliotheques.cirad.fr/cgi-bin/koha/opac-detail.pl?biblionumber=199720>;

  dce:language           "eng";
  dct:language           <http://id.loc.gov/vocabulary/iso639-1/en>;

  rdfs:isDefinedBy       issa:dataset-1-0-20220306;
  prov:generatedAtTime   "2020-11-21T13:17:03Z"^^xsd:dateTime;
  prov:wasDerivedFrom    <http://agritrop.cirad.fr/543654/>.

  issapr:hasBody         <http://data-issa.cirad.fr/article/543654#body_text> ;
  dct:abstract           <http://data-issa.cirad.fr/article/543654#abstract> ;
  issapr:hasTitle        <http://data-issa.cirad.fr/article/543654#title> ;
```

## Thematic descriptors

The global thematic descriptors are concepts characterizing the article as a whole. They are described as **annotations** using the **[Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/)**.

Each annotation consists of the following information:
- the annotation target (`oa:hasTarget`) is the article it is about (`schema:about`)
- the annotation body (`oa:hasBody`) gives the URI of the resource identified as representing the thematic descriptor (e.g. an **[Agrovoc category URI](https://agrovoc.fao.org/)** ).
- provenance 
    - dataset name and version (`rdfs:isDefinedBy`)
    - the software that assigned this descriptor to the article (`prov:wasAttributedTo`)
        - a human documentalist (`issa:AgritropDocumentalist`)
        - an automated indexing system (e.g. **[Annif](https://annif.org/)** ) (`prov:AnnifSubjectIndexer`)
- (optional) an automated indexer confidence score (`issapr:confidence`)
- (optional) an automated indexer rank of the descriptor among all assigned (`issapr:rank`)

	
Example:
```turtle
# sustainable development
<http://data-issa.cirad.fr/descr/3573cd52f16d7882c72210bca7c9b3ecef02d129>
  a                      prov:Entity , issa:ThematicDescriptorAnnotation;
  oa:hasBody             <http://aims.fao.org/aos/agrovoc/c_35332>;
  oa:hasTarget           <http://data-issa.cirad.fr/article/543654>;
  prov:wasAttributedTo   issa:AgritropDocumentalist.
  rdfs:isDefinedBy       issa:dataset-1-0-20220306;
  
# natural resource management  
<http://data-issa.cirad.fr/descr/e2ba273e40beccc2b8ae5f7792690dce7e6b2131>
  a                      prov:Entity , issa:ThematicDescriptorAnnotation;
  oa:hasBody             <http://aims.fao.org/aos/agrovoc/c_9000115>;
  oa:hasTarget           <http://data-issa.cirad.fr/article/543654>;
  prov:wasAttributedTo   issa:AnnifSubjectIndexer.
  rdfs:isDefinedBy       issa:dataset-1-0-20220306;

  issapr:confidence      0.82;
  issapr:rank            1;
```

## Named entities

The named entities identified in an article are described as **annotations** using the **[Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/)**.

Each annotation consists of the following information:
- the article it is about (`schema:about`)
- the annotation target (`oa:hasTarget`) describes the piece of text identified as a named entity as follows:
    - the source (`oa:hasSource`) is the part of the article where the named entity was detected (title, abstract or body)
    - the selecor (`oa:hasSelector`) gives the named entity raw text (`oa:exact`) and its location whithin the source (`oa:start` and `oa:end`)
- the annotation body (`oa:hasBody`) gives the URI of the resource identified as representing the named entity (e.g. a Wikidata URI, DBPedia URI, or Geonames URI)
- provenance
    - dataset name and version (`rdfs:isDefinedBy`)
    - the software that assigned this descriptor to the article (`prov:wasAttributedTo`)
- (optional) domains related to the named entity (`dct:subject`)
- (optional) the annotating tool confidence (`issapr:confidence`)

Example:
```turtle
<http://data-issa.cirad.fr/ann/b46b064a5d1c58e9abea067e77f24c71d3a3e78d>
  a                      prov:Entity , oa:Annotation ;
  rdfs:label             "named entity 'natural resource management'";
  schema:about           <http://data-issa.cirad.fr/article/543654> ;
  dct:subject            "Gas" , "Environment" ;
  issapr:confidence      0.7669;

  oa:hasBody             <http://wikidata.org/entity/Q3743137> ;
  oa:hasTarget [
      oa:hasSource       <http://data-issa.cirad.fr/article/543654#abstract> .
      oa:hasSelector [
          a              oa:TextPositionSelector, oa:TextQuoteSelector;
          oa:exact       "natural resource management";
          oa:end         1760;
          oa:start       1733.
     ]
 ].

  rdfs:isDefinedBy       issa:dataset-1-0-20220306;
  prov:wasAttributedTo   issa:EntityFishing .
```