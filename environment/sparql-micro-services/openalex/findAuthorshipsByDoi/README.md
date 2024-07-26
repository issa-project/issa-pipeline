This SPARQL micro-service retrieves from OpenAlex the authors and institutions of an article given by its DOI (without the `https://doi.org/`).
It then creates a graph whose main resource is the article's URI (given as a parameter).

Authors are given in 3 ways: as literals (`dce:creator`), with their OpenAlex URIs (`dct:creator`) and as an ordered list (`bibo:authorList`).

Similarly, for each author, the institutions are given in 2 ways: with their OpenAlex URIs (`foaf:member`) and as an ordered list (`issapr:institutionList`).

Example invocation of the service:
`http://localhost/service/openalex/findAuthorshipsByDoi?documentDoi=10.1051/cagri/2021015&documentUri=http://data-issa.cirad.fr/document/598930`

Result graph:

```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix wdt: <http://www.wikidata.org/prop/direct/> .
@prefix gn: <http://www.geonames.org/ontology#> .
@prefix dce: <http://purl.org/dc/elements/1.1/> .
@prefix issapr: <http://data-issa.cirad.fr/property/> .
@prefix bibo: <http://purl.org/ontology/bibo/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix dct: <http://purl.org/dc/terms/> .

<https://openalex.org/I1282913463> 
    a foaf:Organization ;
    gn:countryCode "CR" ;
    foaf:name "Centro Agronomico Tropical de Investigacion y Ensenanza Catie" ;
    rdsf:label "Centro Agronomico Tropical de Investigacion y Ensenanza Catie" ;
    wdt:P6782 <https://ror.org/05tkvpg69> .

<https://openalex.org/I108192572> 
    a foaf:Organization ;
    gn:countryCode "CA" ;
    foaf:name "HEC Montréal" ;
    rdsf:label "HEC Montréal" ;
    wdt:P6782 <https://ror.org/05ww3wq27> .

<https://openalex.org/I19894307>
    a foaf:Organization ;
    gn:countryCode "FR" ;
    foaf:name "Université de Montpellier" ;
    rdsf:label "Université de Montpellier" ;
    wdt:P6782 <https://ror.org/051escj72> .

<https://openalex.org/I131077856> 
    a foaf:Organization ;
    gn:countryCode "FR" ;
    foaf:name "Centre de Coopération Internationale en Recherche Agronomique pour le Développement" ;
    rdsf:label "Centre de Coopération Internationale en Recherche Agronomique pour le Développement" ;
    wdt:P6782 <https://ror.org/05kpkpg04> .

<https://openalex.org/I4210126969> 
    a foaf:Organization ;
    gn:countryCode "FR" ;
    foaf:name "Forests and Societies" ;
    rdsf:label "Forests and Societies" ;
    wdt:P6782 <https://ror.org/02pzyz439> .

<https://openalex.org/I4210165284> 
    a foaf:Organization ;
    gn:countryCode "MX" ;
    foaf:name "El Colegio de la Frontera Sur" ;
    rdsf:label "El Colegio de la Frontera Sur" ;
    wdt:P6782 <https://ror.org/05bpb0y22> .

<https://openalex.org/I90183372> 
    a foaf:Organization ;
    gn:countryCode "FR" ;
    foaf:name "Université de Lorraine" ;
    rdsf:label "Université de Lorraine" ;
    wdt:P6782 <https://ror.org/04vfs2w97> .


<https://openalex.org/A5012529571> 
    a foaf:Person ;
    rdfs:label "Colombine Lesage" ;
    foaf:name "Colombine Lesage" ;
    wdt:P496 <https://orcid.org/0000-0003-3329-4247> ;
    issapr:institutionList ( <https://openalex.org/I131077856> <https://openalex.org/I108192572> <https://openalex.org/I90183372> <https://openalex.org/I4210126969> ) .

<https://openalex.org/A5053856480> 
    a foaf:Person ;
    issapr:institutionList ( <https://openalex.org/I4210165284> <https://openalex.org/I4210126969> <https://openalex.org/I131077856> ) ;
    rdfs:label "Jaime Andrés Cifuentes-Espinosa" ;
    foaf:name "Jaime Andrés Cifuentes-Espinosa" ;
    wdt:P496 <https://orcid.org/0000-0003-4744-1607> .

<https://openalex.org/A5011188920> 
    a foaf:Person ;
    rdfs:label "Laurène Feintrenie" ;
    foaf:name "Laurène Feintrenie" ;
    wdt:P496 <https://orcid.org/0000-0003-1621-396X> ;
    issapr:institutionList ( <https://openalex.org/I1282913463> <https://openalex.org/I4210126969> <https://openalex.org/I19894307> <https://openalex.org/I131077856> ) .


<http://data-issa.cirad.fr/document/598930> 
    dce:creator "Colombine Lesage" ;
    dce:creator "Jaime Andrés Cifuentes-Espinosa" ;
    dce:creator "Laurène Feintrenie" ;
    dct:creator <https://openalex.org/A5012529571> ;
    dct:creator <https://openalex.org/A5053856480> ;
    dct:creator <https://openalex.org/A5011188920> ;
    bibo:authorList ( <https://openalex.org/A5012529571> <https://openalex.org/A5053856480> <https://openalex.org/A5011188920> ) .
```