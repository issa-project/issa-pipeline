# ISSA RDF data modeling

A document analyzed by the ISSA pipeline can be described in three parts: general metadata (title, authors, publication date etc.), thematic descriptors characterizing a document as well as documents domains and authors' keywords, and named entities extracted from a document's parts (title, abstract, body_text).

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

>:point_right: The namespace *http://data-issa.cirad.fr/* is used for a specific ISSA instance (e.g. Agritrop). It can be replaced by any other namespace.


## Document metadata

Document URIs are formatted as `http://data-issa.cirad.fr/document/document_id` where document_id is a unique document identifier.

RDF resources representing documents can be instances of various classes depending on their type:

- article (`fabio:ResearchPaper`, `schema:ScholarlyArticle`, `bibo:AcademicArticle`, `eprint:JournalArticle`)
- conference article (`fabio:ConferencePaper`, `eprint:ConferencePaper`)
- book (`fabio:Book`, `bibo:Book`, `eprint:Book`)
- book section (`fabio:BookChapter`, `bibo:BookSection`, `eprint:BookItem`)
- thesis (`fabio:Thesis`, `bibo:Thesis`, `eprint:Thesis`)
- application (`fabio:ComputerApplication`)
- data management plan (`fabio:DataManagementPlan`)
- film (`fabio:Film` , `bibo:AudioVisualDocument`)
- map (`fabio:StillImage`, `bibo:Map`)
- monograph (`fabio:Expression`, `bibo:Document`, `eprint:Text`)
- patent (`fabio:Patent`, `eprint:Patent`)
- report (`fabio:Report`, `bibo:Report`, `eprint:Report`)
- review (`fabio:Review`)

For each document, the available metadata are mapped as much as possible as follows (not all metadata exist for all types of documents):

- title (`dct:title`)
- authors (`dce:creator`)
- authors in ordered list (`bibo:authorList`)
- publication date (`dct:issued`)
- journal (`schema:publication`)
- license (`dct:license`)
- access rights (`dct:accessRights`)
- terms and conditions (`dct:rights`)
- identifiers
    - archive internal identifier (`dct:identifier`)
    - DOI (`bibo:doi`)
- source (API) from which the metadata information was retrieved (`dct:source`)
- document page URL (`schema:url`)
- source PDF download URL (`schema:downloadUrl`)
- alternate PDF download URLs (`schema:sameAs`)
- language
    - language string (`dce:language`)
    - language URI (`dct:language`)
- provenance
    - dataset name and version (`rdfs:isDefinedBy`)
    - source data URI (`prov:wasDerivedFrom`)
    - source data creation timestamp (`prov:generatedAtTime`), i.e. at which time the article was added to the source archive

Furthermore, documents are linked to their parts (title, abstract, body) as follows:
- `issapr:hasTitle <http://data-issa.cirad.fr/document/paper_id#title>`
- `dct:abstract   <http://data-issa.cirad.fr/document/paper_id#abstract>`
- `issapr:hasBody  <http://data-issa.cirad.fr/document/paper_id#body_text>`.

>:point_right: In the Agritrop use case only journal articles have associated body text


Here is an example of a journal article's metadata:

```turtle
<http://data-issa.cirad.fr/document/543654>
  a                      prov:Entity, fabio:ResearchPaper, bibo:AcademicArticle, eprint:JournalArticle, schema:ScholarlyArticle;
  dct:title              "Accounting for the ecological dimension in participatory research and development : lessons learned from Indonesia and Madagascar";
  dce:creator            "Pfund, Jean-Laurent", "Laumonier, Yves", "Bourgeois, Robin";
  bibo:authorList        [ a       rdf:List ;
                            rdf:first "Laumonier, Yves" ;
                            rdf:rest ("Bourgeois, Robin" "Pfund, Jean-Laurent")
                         ] ;
  
  schema:publication     "Ecology and Society";
  dct:issued             "2008.0"^^xsd:gYear;

  dct:accessRights       <info:eu-repo/semantics/openAccess> ;
  dct:rights             <https://agritrop.cirad.fr/mention_legale.html>;

  dct:identifier         "543654";
  
  schema:url             <http://agritrop.cirad.fr/543654/> ;
  schema:downloadUrl     <http://agritrop.cirad.fr/543654/1/document_543654.pdf>;
  schema:sameAs          <http://www.ecologyandsociety.org/vol13/iss1/art15/>;

  dce:language           "eng";
  dct:language           <http://id.loc.gov/vocabulary/iso639-1/en>;

  rdfs:isDefinedBy       issa:issa-agritrop;
  prov:generatedAtTime   "2020-11-21T13:17:03Z"^^xsd:dateTime;
  prov:wasDerivedFrom    <http://agritrop.cirad.fr/543654/>.

  issapr:hasTitle        <http://data-issa.cirad.fr/document/543654#title> ;
  dct:abstract           <http://data-issa.cirad.fr/document/543654#abstract> ;
  issapr:hasBody         <http://data-issa.cirad.fr/document/543654#body_text> .
```

## Thematic descriptors

The thematic descriptors are concepts characterizing a document as a whole. They are described as **annotations** using the **[Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/)**.

Each annotation consists of the following information:

- the annotation target (`oa:hasTarget`) is the document it is about (`schema:about`)
- the annotation body (`oa:hasBody`) gives the URI of the resource identified as representing the thematic descriptor (e.g. an **[Agrovoc category URI](https://agrovoc.fao.org/)** ).
- provenance 
    - dataset name and version (`rdfs:isDefinedBy`)
    - the agent that assigned this descriptor to a document (`prov:wasAttributedTo`)
        - a human documentalist (`issa:Documentalist`)
        - an automated indexing system (e.g. **[Annif](https://annif.org/)** ) (`issa:AnnifSubjectIndexer`)
- (optional) an automated indexer confidence score (`issapr:confidence`)
- (optional) an automated indexer rank of the descriptor among all assigned (`issapr:rank`)

	
Example:

```turtle
# sustainable development
<http://data-issa.cirad.fr/descr/3573cd52f16d7882c72210bca7c9b3ecef02d129>
  a                      prov:Entity , issa:ThematicDescriptorAnnotation;
  oa:hasBody             <http://aims.fao.org/aos/agrovoc/c_35332>;
  oa:hasTarget           <http://data-issa.cirad.fr/document/543654>;
  prov:wasAttributedTo   issa:Documentalist.
  rdfs:isDefinedBy       issa:issa-agritrop.
  
# natural resource management  
<http://data-issa.cirad.fr/descr/e2ba273e40beccc2b8ae5f7792690dce7e6b2131>
  a                      prov:Entity , issa:ThematicDescriptorAnnotation;
  oa:hasBody             <http://aims.fao.org/aos/agrovoc/c_9000115>;
  oa:hasTarget           <http://data-issa.cirad.fr/document/543654>;
  prov:wasAttributedTo   issa:AnnifSubjectIndexer.
  rdfs:isDefinedBy       issa:issa-agritrop;

  issapr:confidence      0.82;
  issapr:rank            1.
```

>:point_right: In the ISSA Agritrop instance some of the Agrovoc categories are geographical entities (e.g. countries, regions, cities) and can be categorized as Geographical (Geo) descriptors. To identify if a descriptor has a geographical meaning, the following SPARQL query can be used:

```turtle
  OPTIONAL {
      ?descriptorUri <http://aims.fao.org/aos/agrontology#isPartOfSubvocabulary> ?subVocabulary .
      BIND ( REGEEX ?subVocabulary, "^Geographical", "i") as ?isGeographicalDescriptor )
  }
```

## Domains

Each source archive may associate a set of domains with each document. The domains are can be  proprietary (e.g. [AgrIST-thema](https://agrist.cirad.fr/agrist-thema) in Agritrop) or controlled vocabularies (e.g. [HAL subjects](https://aurehal.archives-ouvertes.fr/domain/index) in HAL).

The domain annotation consists of the following information:

- the annotation target (`oa:hasTarget`) is a document
- the annotation body (`oa:hasBody`) is the URI of the resource representing the domain
- provenance 
    - dataset name and version (`rdfs:isDefinedBy`)
    - the agent that assigned this descriptor to a document (`prov:wasAttributedTo`) and typically is a human documentalist (`issa:Documentalist`)
- (optional) an automated indexer rank of the descriptor among all assigned (`issapr:rank`)

Example:

```turtle
<http://data-issa.cirad.fr/descr/9f429daf638f56790cf3e587816ead1667537e98>
  a                      prov:Entity , issa:DomainAnnotation ;
  oa:hasBody             <http://agrist.cirad.fr/agrist-thema/K01> ;
  oa:hasTarget           <http://data-issa.cirad.fr/document/543654> ;
  rdfs:isDefinedBy       issa:issa-agritrop ;
  prov:wasAttributedTo   issa:Documentalist ;

  issapr:rank            3.

<http://agrist.cirad.fr/agrist-thema/K01>
  rdfs:label             "K01 - Foresterie - Considérations générales". 
```

## Authors Keywords

Some of the document archives (e.g. HAL) may provide a list of keywords assigned by the authors of a document. These keywords are described as **annotations** as well.

```turtle
<http://data-issa.euromov.fr/descr/f71f792c418b4a959b798d06367453b4b9005d0b>
  a                      prov:Entity , issa:AuthorKeywordAnnotation ;
  oa:hasBody             <http://data-issa.euromov.fr/keywords/f71f792c418b4a959b798d06367453b4b9005d0b> ;
  oa:hasTarget           <http://data-issa.euromov.fr/document/hal-03598013v1> ;
  rdfs:isDefinedBy       issa:issa-hal-euromov ;
  prov:wasAttributedTo   issa:Author;

  issapr:rank            3.

<http://data-issa.euromov.fr/keywords/f71f792c418b4a959b798d06367453b4b9005d0b>
  a                      oa:TextualBody ;
  rdf:value              "Coronavirus" ;
  dct:format             "text" ;
  dct:language           "en".
```

## Named entities

The named entities identified in a document are described as **annotations** using the **[Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/)**.

Each annotation consists of the following information:
- the document it is about (`schema:about`)
- the annotation target (`oa:hasTarget`) describes the piece of the text identified as a named entity as follows:
    - the source (`oa:hasSource`) is a part of a document  where the named entity was detected (title, abstract, or body)
    - the selecor (`oa:hasSelector`) gives the named entity raw text (`oa:exact`) and its location whithin the source (`oa:start` and `oa:end`)
- the annotation body (`oa:hasBody`) gives the URI of the resource identified as representing the named entity (e.g. a Wikidata URI, DBPedia URI, or Geonames URI)
- provenance
    - dataset name and version (`rdfs:isDefinedBy`)
    - the software that assigned this named entity to the document (`prov:wasAttributedTo`)
- (optional) domains related to the named entity (`dct:subject`)
- (optional) the annotating tool confidence (`issapr:confidence`)

Example:
```turtle
<http://data-issa.cirad.fr/ann/b46b064a5d1c58e9abea067e77f24c71d3a3e78d>
  a                      prov:Entity , oa:Annotation ;
  rdfs:label             "named entity 'natural resource management";
  schema:about           <http://data-issa.cirad.fr/document/543654> ;
  dct:subject            "Gas" , "Environment" ;
  issapr:confidence      0.7669;

  oa:hasBody             <http://wikidata.org/entity/Q3743137> ;
  oa:hasTarget [
      oa:hasSource       <http://data-issa.cirad.fr/document/543654#abstract> .
      oa:hasSelector [
          a              oa:TextPositionSelector, oa:TextQuoteSelector;
          oa:exact       "natural resource management";
          oa:end         1760;
          oa:start       1733.
     ]
 ].

  rdfs:isDefinedBy       issa:issa-agritrop;
  prov:wasAttributedTo   issa:EntityFishing .
```
