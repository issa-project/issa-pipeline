#!/usr/bin/env python
# coding: utf-8

# # ISSA-2: convert the AgrIST- Disciplines thesaurus from the Excel to RDF 
# 
# Note: *rdflib* does not output the triples in the order they are added, we slightly modify the serialization from a straight forward way. 

# In[233]:


import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDF, SKOS, RDFS, DCTERMS, XSD, VOID, DCAT, FOAF
import datetime
import re


# In[234]:


agrist_fn = 'Referentiel_scientifique_Cirad_2005_20231023.xlsx'
agrist_df = pd.read_excel(agrist_fn, 0, 
                          usecols='A:G',
                          #skiprows=1,
                          dtype='str',
                          names=['domain', 'domain-label-fr',
                                 'discipline', 'discipline-label-fr',
                                 'speciality', 'speciality-label-fr',
                                 'scopeNote'],
                          index_col=None)

schema_title_en = u'AgrIST-Disciplines classification'
schema_title_fr = u'Référentiel disciplinaire du Cirad'

# this comment is needed to put the rdfs prefix as early as posible 
schema_comment = u'Plan de classement AgrIST-Disciplines - Version du 23 octobre 2023'
schema_description = u'Le référentiel scientifique du Cirad (Centre de coopération internationale en recherche agronomique pour le développement) a été élaboré en 2005 pour caractériser les domaines, les champs disciplinaires et les spécialités des personnels scientifiques du Cirad'

schema_creator     = 'https://ror.org/05kpkpg04' #CIRAD
schema_contributor = 'https://ror.org/02kvxyf05' #INRIA

schema_version = '2023.10.23'
schema_created = '2005'
schema_issued  = '2005'
schema_modified = datetime.datetime.now().strftime('%Y-%m-%d')

schema_license = 'https://creativecommons.org/licenses/by-nc/4.0/'
schema_access =  'http://purl.org/eprint/accessRights/OpenAccess'

schema_doi = 'https://doi.org/10.18167/DVN1/JWPHJZ'
schema_contact = 'mailto:dist-com@cirad.fr'
#sparql_endpoint = 'https://data-issa.cirad.fr/sparql'


agrist_ttl = 'AgrIST-Disciplines-v20231023.ttl'
agrist_ns = 'http://agrist.cirad.fr/agrist-disciplines/'
agrist_schema = agrist_ns


# In[235]:


#agrist_df.loc[agrist_df['category'].str[0] == 'Y', 'sub-category'] = ''

agrist_df['domain'] = agrist_df['domain'].fillna(method='ffill')
agrist_df['domain-label-fr'] = agrist_df['domain-label-fr'].fillna(method='ffill')
agrist_df['discipline'] = agrist_df['discipline'].fillna(method='ffill')
agrist_df['discipline-label-fr'] = agrist_df['discipline-label-fr'].fillna(method='ffill')

agrist_df['domain'] = agrist_df['domain'].str.replace(' ','')
agrist_df['discipline-label-fr'] = agrist_df['discipline-label-fr'].str.replace('\n',' ')
agrist_df['discipline-label-fr'] = agrist_df['discipline-label-fr'].str.replace('  ',' ')
agrist_df['discipline-label-fr'] = agrist_df['discipline-label-fr'].str.replace('"','\'')
agrist_df['discipline-label-fr'] = agrist_df['discipline-label-fr'].str.strip()

agrist_df['speciality-label-fr'] = agrist_df['speciality-label-fr'].str.replace('\n',' ')
agrist_df['speciality-label-fr'] = agrist_df['speciality-label-fr'].str.replace('  ',' ')
agrist_df['speciality-label-fr'] = agrist_df['speciality-label-fr'].str.replace('"','\'')
agrist_df['speciality-label-fr'] = agrist_df['speciality-label-fr'].str.strip()

agrist_df['scopeNote'] = agrist_df['scopeNote'].str.replace('\n',' ')
agrist_df['scopeNote'] = agrist_df['scopeNote'].str.replace('"','\'')
agrist_df['scopeNote'] = agrist_df['scopeNote'].str.strip()


# In[236]:


agrist_df.dropna(inplace=True)


# #### start the graph with namespaces

# In[237]:


def new_Graph(agrist_ns = 'https://agrist.cirad.fr/'):
    g = Graph()

    g.bind('skos', SKOS)
    g.bind('dc', DC)
    g.bind('dct', DCTERMS)
    g.bind('rdfs', RDFS)
    g.bind('dcat', DCAT)
    g.bind('void', VOID)
    g.bind('foaf', FOAF)
    g.bind('agrist-disciplines', Namespace(agrist_ns))
    
    return g


# Using explicit write to the file instead of rdflib serialization to the file 
# to create a better ordered file
def serialize_Graph(g, file_name=agrist_ttl, append=False):
    if not append:

        with open(file_name, 'bw') as ttl_file:
            ttl_file.write(g.serialize(format='turtle'))
    else:

        def _remove_prefixes(g):
            return g.serialize(format="turtle").decode('utf-8').split('\n\n', maxsplit=1)[1].encode('utf-8') 

        with open(file_name, 'ba') as ttl_file:
            ttl_file.write(_remove_prefixes(g))
        


# #### define schema

# In[238]:


g = new_Graph(agrist_ns)
schema=URIRef(agrist_schema) 

g.add( (schema , RDF.type, SKOS.ConceptScheme ))
g.add( (schema , RDFS.comment, Literal(schema_comment, lang='fr') ))

g.add( (schema , DC.title, Literal(schema_title_fr, lang='fr') ))
#g.add( (schema , DC.title, Literal(schema_title_en, lang='en') ))


# metadata
g.add( (schema , DCTERMS.creator,     URIRef(schema_creator)    )) 
g.add( (schema , DCTERMS.contributor, URIRef(schema_contributor))) 
g.add( (schema , DCTERMS.publisher,   URIRef(schema_creator)  ))
g.add( (schema , DCTERMS.publisher,   URIRef(schema_contributor)  ))

g.add( (schema , DCTERMS.created,  Literal(schema_created, datatype=XSD.gYear)) )
g.add( (schema , DCTERMS.isssued,  Literal(schema_created, datatype=XSD.gYear)) )
g.add( (schema , DCTERMS.modified, Literal(schema_modified, datatype=XSD.date)) )

g.add( (schema , DCTERMS.license , URIRef(schema_license) )) 
g.add( (schema , DCTERMS.accessRights, URIRef(schema_access) )) 

#g.add( (schema , VOID.sparqlEndpoint, URIRef(sparql_endpoint) ))
g.add( (schema , VOID.uriSpace , URIRef(agrist_ns) ))

g.add( (schema , DCAT.version , Literal(schema_version) ))

g.add( (schema , DCTERMS.identifier , URIRef(schema_doi) ))
g.add( (schema , FOAF.mbox , URIRef(schema_contact) ))
g.add( (schema , DCTERMS.description , Literal(schema_description, lang='fr') ))


# In[248]:


XSD.gYear


# In[239]:


print(g.serialize(format="turtle").decode('utf-8'))


# In[240]:


serialize_Graph(g, agrist_ttl)


# #### define top concepts (categories)

# In[241]:


g = new_Graph(agrist_ns)

for ind, row in agrist_df.drop_duplicates(subset=['discipline','discipline-label-fr']).iterrows():

    domain = URIRef(agrist_ns + row['domain'])
    lbl_fr   = Literal(row['domain-label-fr'], lang='fr') 

    g.add( (domain , RDF.type, SKOS.Concept ))
    g.add( (domain , SKOS.topConceptOf, schema ))
    g.add( (domain , SKOS.prefLabel,  lbl_fr))

    
    discipline = URIRef(agrist_ns + row['discipline'])
    lbl_fr   = Literal(row['discipline-label-fr'], lang='fr')
    
    g.add( (discipline , RDF.type, SKOS.Concept ))
    g.add( (discipline , SKOS.broader, domain ))
    g.add( (discipline , SKOS.prefLabel,  lbl_fr))


# In[242]:


print(g.serialize(format="turtle").decode('utf-8'))


# In[243]:


serialize_Graph(g, agrist_ttl, append=True)


# #### define all concepts (sub-categories) 

# In[244]:


g = new_Graph(agrist_ns)
for ind, row in agrist_df.iterrows():
    
    if len(row['speciality']) > 0:
    
        category = URIRef(agrist_ns + row['discipline'])
        speciality = URIRef(agrist_ns + row['speciality'])
        lbl_fr   = Literal(row['speciality-label-fr'], lang='fr')
        scope_note   = Literal(row['scopeNote'], lang='fr')

        g.add( (speciality , RDF.type, SKOS.Concept ))
        g.add( (speciality , SKOS.broader, category ))
        g.add( (speciality , SKOS.prefLabel,  lbl_fr))
        g.add( (speciality , SKOS.scopeNote,  scope_note))
    #else:
    #    category = URIRef(agrist_ns + row['category'])
    #    editorial_note   = Literal(row['editorialNote'], lang='fr')
    #    g.add( (category , SKOS.editorialNote,  editorial_note))


# In[245]:


print(g.serialize(format="turtle").decode('utf-8'))


# In[246]:


serialize_Graph(g, agrist_ttl, append=True)


# In[ ]:




