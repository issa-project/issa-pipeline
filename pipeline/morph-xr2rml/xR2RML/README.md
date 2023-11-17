To transform data collected in the metadata, indexing and annotation steps that are generally represented in JSON format  into [RDF](https://www.w3.org/RDF/) we use [Morph-xR2RML](https://github.com/frmichel/morph-xr2rml) tool. This tool takes the following input:

- a [database query](https://www.mongodb.com/docs/manual/tutorial/query-documents/) as data input
- [R2RML](https://www.w3.org/TR/r2rml/) mapping language templates as transformation instructions.

In ISSA we chose to use MongoDB as an intermediate queryable database storage as the most suitable for the JSON import, see [mongo](../mongo) for details.

This folder provides the scripts, configuration and mappings files needed for transformation to RDF:

- script [run-transformation.sh](./run-transformation.sh) is the main entry point. Comment or uncomment the lines as needed.
- the configuration xR2RML.properies for Java applications contain the *database.name* parameter that defines the name of the database to be read for transformation.

>:point_right: Since each update of ISSA dataset is stored in a separate database one parameter *database.name* of `xR2RML.properties` will be assigned __automatically__ to the latest update  defined in [env.sh](../../env.sh).

- the Turtle files _*.tpl.ttl_ provide the mapping between fields in a database collection and RDF triples, *subjects* and *objects*, to build a desired knowledge graph. For simplicity, each template file corresponds to one collection in the database.

Each template file contains placeholders that serve as "parameters":

- `{{dataset}}` - RDF dataset name for provenance
- `{{collection}}` - MongoDB database collection name
- `{{namespace}}` - ISSA instance specific namespace, .e.g. _http://data-issa.cirad.fr_

To reduce the size of RDF files for annotations the _*annot.tpl.ttl_ mappings are done per article part (title, abstract, body text) and take an extra parameter:

- `{{documentpart}}` - article part name (title, abstract, body_text)


Example of xR2EML transformation:

<table> <tbody>
<tr><td>Input JSON</td><td><pre>
{ "paper_id" : "123456", 
  "title" :"The irreversible momentum of clean energy", 
  "authors": ["Obama, Barack"]  } </pre></td></tr>
<tr><td>xR2RML mapping</td><td><pre>
<#LS> 
   a xrr:LogicalSource;   
   xrr:query """db.metadata.find( { paper_id: { $exists: true} } )""".
<#TM> 
   a rr:TriplesMap; 
   xrr:logicalSourse <#LS>;
   rr:subjectMap [
            rr:template "http://example.org/article/{$.paper_id}"   ];        
   rr:predicateObjectMap [ 
           rr:predicate dct:title; 
           rr:objectMap [ xrr:reference "$.title"; ];   ];
   rr:predicateObjectMap [
           rr:predicate dca:creator;
           rr:objectMap [ xff:reference "$.authors.*"; ] ].</pre> </td></tr>
<tr><td>Output RDF</td><td><pre>
&lthttp://example.org/article/123456&gt dct:title "Irreversible momentum of clean energy".
&lthttp://example.org/article/123456&gt dca:creator "Obama, Barack". </pre> </td></tr>
</tbody></table>
