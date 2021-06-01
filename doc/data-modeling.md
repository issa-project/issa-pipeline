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
@prefix foaf:   <http://xmlns.com/foaf/0.1/>.
@prefix frbr:   <http://purl.org/vocab/frbr/core#>.
@prefix oa:     <http://www.w3.org/ns/oa#>.
@prefix prov:   <http://www.w3.org/ns/prov#>.
@prefix schema: <http://schema.org/>.

@prefix issap:  <http://ns.inria.fr/issa/property/> .
```

## Article metadata
Article URIs are formatted as http://ns.inria.fr/issa/article_id where article_id is a unique article identifier.

Article metadata may include the following items:
- title (`dct:title`)
- authors (`dce:creator`)
- publication date (`dct:issued`)
- journal (`schema:publication`)
- license (`dct:license`)
- identifiers
    - DOI (`bibo:doi`)
    - Pubmed identifer (`bibo:pmid` and `fabio:hasPubMedId`)
    - PMC identifer (`fabio:hasPubMedCentralId`)
- source of the metadata information (`dct:source`)
- DOI-based URL (`schema:url`)
- language string (` dce:language `)
- language URI (`dct:language`)

Furthermore, each article is linked to its parts (title, abstract, body) as follows:
- `issap:hasTitle <http://ns.inria.fr/issa/paper_id#title>`
- `dct:abstract   <http://ns.inria.fr/issa/paper_id#abstract>`
- `issap:hasBody  <http://ns.inria.fr/issa/paper_id#body_text>`.

Here is an example of article metadata:
```turtle
<http://ns.inria.fr/issa/f74923b3ce82c984a7ae3e0c2754c9e33c60554f>
  a                         schema:ScholarlyArticle, bibo:AcademicArticle, fabio:ResearchPaper ;
  rdfs:isDefinedBy          <http://ns.inria.fr/issa/dataset-1-2> ;
  
  dct:title                 "A real-time PCR for SARS-coronavirus incorporating target gene pre-amplification" ;
  dce:creator                "Tam, Siu-Lun", "Lin, Sau-Wah", "Yu, -H", "Collins, Richard", "Chan, Paul", "Wong, Freda Pui-Fan", "Dillon, Natalie", "Fung, Yin-Wan", "Cheung, Albert", "Yu, -Hoi", "Li, Hui", "Wang, Chen", "Lau,", "Lok, Ting" ;
  dct:issued                "2003-12-26"^^xsd:date ;
  dct:license               "els-covid" ;
  schema:url                <https://doi.org/10.1016/j.bbrc.2003.11.064> ;
  dct:source                "Elsevier; Medline; PMC" ;
  schema:publication        "Biochemical and Biophysical Research Communications" ;

  bibo:doi                  "10.1016/j.bbrc.2003.11.064" ;
  bibo:pmid                 "14652014" ;
  fabio:hasPubMedCentralId "PMC7111096" ;
  fabio:hasPubMedId         "14652014" ;
  
  dct:language              <http://id.loc.gov/vocabulary/iso639-1/en>;
  dce:language              "eng";
  
  issap:hasTitle            <http://ns.inria.fr/issa/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#title> ;
  dct:abstract              <http://ns.inria.fr/issa/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#abstract> ;
  issap:hasBody             <http://ns.inria.fr/issa/f74923b3ce82c984a7ae3e0c2754c9e33c60554f#body_text> .
 
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
    rdfs:isDefinedBy    <http://ns.inria.fr/issa/dataset-1-2> ;
    dct:creator         <https://team.inria.fr/wimmics/> ;
    
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
