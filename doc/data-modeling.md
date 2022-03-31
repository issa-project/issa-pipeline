# ISSA RDF data modeling

An article analyzed by ISSA is described in three parts: general metadata (title, authors, publication date etc.), global descriptors characterizing the article, and the named entities extracted from the article text.


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

## Article metadata
Article URIs are formatted as http://data-issa.cirad.fr/article/article_id where article_id is a unique article identifier.

Article metadata may include the following items:
- title (`dct:title`)
- authors (`dce:creator`)
- publication date (`dct:issued`)
- journal (`schema:publication`)
- license (`dct:license`)
- terms and conditions (`dct:rights`)
- identifiers
    - source id (`dct:identifier`)
    - DOI (`bibo:doi`)
- source of the metadata information (`dct:source`)
- article page URL, possibly DOI-based (`schema:url`)
- source PDF download URL (`schema:downloadUrl`)
- other PDF download URLs (`schema:sameAs`)
- language
    - language string (`dce:language`)
    - language URI (`dct:language`)
- provenance
    - dataset name and version (`rdfs:isDefinedBy`)
    - source data URI (`prov:wasDerivedFrom`)
    - source data creation timestamp (`prov:generatedAtTime`)

Articles can be one of the followng types:
- article type (`rdfs:Class`)
    - journal article (`fabio:ResearchPaper`, `schema:ScholarlyArticle`, `bibo:AcademicArticle`, `eprint:JournalArticle`)
    - application (`fabio:ComputerApplication`)
    - book (`fabio:Book`, `eprint:Book`)
    - book section (`fabio:BookChapter`, `eprint:BookItem`)
    - conference paper (`fabio:ConferencePaper`, `eprint:ConferencePaper`)
    - film (`fabio:Film`)
    - map (`bibo:Map`)
    - monograph (`fabio:Expression`, `bibo:Document`)
    - patent (`fabio:Patent`, `eprint:Patent`)
    - data management plan (`fabio:DataManagementPlan`)
    - thesis (`fabio:Thesis`, `eprint:Thesis`)
)


Furthermore, each article is linked to its parts (title, abstract, body) as follows:
- `issapr:hasTitle <http://data-issa.cirad.fr/article/paper_id#title>`
- `dct:abstract   <http://data-issa.cirad.fr/article/paper_id#abstract>`
- `issapr:hasBody  <http://data-issa.cirad.fr/article/paper_id#body_text>`.
NOTE: only journal articles have associated body text 


Here is an example of article metadata:
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
  schema:downloadUrl     <http://agritrop.cirad.fr/543654/1/document_543654.pdf> ;
  schema:sameAs          <http://www.ecologyandsociety.org/vol13/iss1/art15/>, <http://catalogue-bibliotheques.cirad.fr/cgi-bin/koha/opac-detail.pl?biblionumber=199720> ;

  dce:language           "eng";
  dct:language           <http://id.loc.gov/vocabulary/iso639-1/en>;

  rdfs:isDefinedBy       issa:issa-latest ;
  prov:generatedAtTime   "2020-11-21T13:17:03Z"^^xsd:dateTime ;
  prov:wasDerivedFrom    <http://agritrop.cirad.fr/543654/> .

  issapr:hasBody         <http://data-issa.cirad.fr/article/543654#body_text> ;
  dct:abstract           <http://data-issa.cirad.fr/article/543654#abstract> ;
  issapr:hasTitle        <http://data-issa.cirad.fr/article/543654#title> ;
```

## Global descriptors

The global descriptors are concepts characterizing the article as a whole. They are described as **annotations** using the **[Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/)**.
Each annotation consists of the following information:
- the annotation target (`oa:hasTarget`) is the article it is about (`schema:about`)
- the annotation body (`oa:hasBody`) gives the URI of the resource identified as representing the global descriptor (e.g. a Wikidata URI)
- (optional) domains related to the named entity (`dct:subject`)

Example:
```turtle
<http://ns.inria.fr/issa/ann/51b42903ea45962283bc9a070d9fae14170c95a5_d>
    a                   oa:Annotation, prov:Entity;
    rdfs:label          "descriptor 'coronavirus'" ;
    oa:hasBody          <http://www.wikidata.org/entity/Q82069695> ;
    oa:hasTarget        <http://ns.inria.fr/issa/f74923b3ce82c984a7ae3e0c2754c9e33c60554f> .
```

## Named entities

The named entities identified in an article are described as **annotations** using the **[Web Annotations Vocabulary](https://www.w3.org/TR/annotation-vocab/)**.
Each annotation consists of the following information:
- the article it is about (`schema:about`)
- the annotation target (`oa:hasTarget`) describes the piece of text identified as a named entity as follows:
    - the source (`oa:hasSource`) is the part of the article where the named entity was detected (title, abstract or body)
    - the selecor (`oa:hasSelector`) gives the named entity raw text (`oa:exact`) and its location whithin the source (`oa:start` and `oa:end`)
- the annotation body (`oa:hasBody`) gives the URI of the resource identified as representing the named entity (e.g. a Wikidata URI)
- (optional) domains related to the named entity (`dct:subject`)

Example:
```turtle
<http://ns.inria.fr/issa/ann/f71dbe6cf7b010b170679e250c779c2b0e93325d>
    a                   oa:Annotation, prov:Entity;
    rdfs:label          "named entity 'PCR'" ;
    schema:about        <http://ns.inria.fr/issa/f74923b3ce82c984a7ae3e0c2754c9e33c60554f>;
    dct:subject         "Engineering", "Biology";
    issapr:confidence	"1"^^xsd:decimal;
    
    oa:hasBody          <http://wikidata.org/entity/Q176996>;
    oa:hasTarget [
        oa:hasSource    <http://ns.inria.fr/issa/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#abstract>;
        oa:hasSelector  [
            a           oa:TextPositionSelector, oa:TextQuoteSelector;
            oa:exact    "PCR";
            oa:start    "235";
            oa:end      "238"
        ]
    ];
```