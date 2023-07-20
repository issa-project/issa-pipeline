#!/usr/bin/env python
# coding: utf-8

# # ISSA-2: convert the AgrIST- Filières thesaurus from the Excel to RDF 
# 
# Note: *rdflib* does not output the triples in the order they are added, we slightly modify the serialization from a straight forward way. 

# In[71]:


import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDF, SKOS, RDFS, DCTERMS, XSD, VOID, DCAT
import datetime
import re


# In[72]:


agrist_fn = 'Plan-AgrIST-Filieres_20221205.xlsx'
agrist_df = pd.read_excel(agrist_fn, 0, 
                          usecols='A:D',
                          skiprows=1,
                          names=['sector', 'category', # 'category-label-fr', 'category-label-en',
                                 'sub-category', #'sub-category-label-fr', 'sub-category-label-en',
                                 'editorialNote'],
                          index_col=None)

schema_title_en = u'AgrIST-Filieres classification'
schema_title_fr = u'Plan de classification AgrIST-Filières'

# this comment is needed to put the rdfs prefix as early as posible 
schema_comment = u'Plan de classement AgrIST-Filières - Version du 5 décembre 2022'

schema_creator     = 'https://ror.org/05kpkpg04' #CIRAD
schema_contributor = 'https://ror.org/02kvxyf05' #INRIA

schema_version = '2022.12.05'
schema_created = '2023-07-03'
schema_issued  = '2023-07-03'
schema_modified = datetime.datetime.now().strftime('%Y-%m-%d')

schema_license = 'https://creativecommons.org/licenses/by-nc/4.0/'
schema_access =  'http://purl.org/eprint/accessRights/OpenAccess'

sparql_endpoint = 'https://data-issa.cirad.fr/sparql'

agrist_ttl = 'AgrIST-Filieres-v20230523.ttl'
agrist_ns = 'https://agrist.cirad.fr/agrist-filieres/'
agrist_schema = agrist_ns


# In[73]:


agrist_df.loc[agrist_df['category'].str[0] == 'Y', 'sub-category'] = ''

agrist_df['sector'] = agrist_df['sector'].fillna(method='ffill')
agrist_df['category'] = agrist_df['category'].fillna(method='ffill')

agrist_df = agrist_df.dropna(subset='sub-category').apply(lambda x: x.str.strip()).fillna('')


# In[74]:


# create labels
agrist_df['sector-label-fr'] = agrist_df['sector'].apply(lambda x: x.split(' ', maxsplit=1)[1] )
agrist_df['sector'] = agrist_df['sector'].str[0]

agrist_df['category-label-fr'] = agrist_df['category'].apply(lambda x: x.split(' ', maxsplit=1)[1] )
agrist_df['category'] = agrist_df['category'].str[:2]

agrist_df['sub-category-label-fr'] = agrist_df['sub-category'].apply(lambda x: x.split(' ', maxsplit=1)[1] if len(x) > 0 else '')
agrist_df['sub-category'] = agrist_df['sub-category'].str[:3]


# #### start the graph with namespaces

# In[75]:


def new_Graph(agrist_ns = 'https://agrist.cirad.fr/'):
    g = Graph()

    g.bind('skos', SKOS)
    g.bind('dc', DC)
    g.bind('dct', DCTERMS)
    g.bind('rdfs', RDFS)
    g.bind('dcat', DCAT)
    g.bind('void', VOID)
    g.bind('agrist-filieres', Namespace(agrist_ns))
    
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

# In[76]:


g = new_Graph(agrist_ns)
schema=URIRef(agrist_schema) 

g.add( (schema , RDF.type, SKOS.ConceptScheme ))
g.add( (schema , RDFS.comment, Literal(schema_comment, lang='fr') ))

g.add( (schema , DC.title, Literal(schema_title_fr, lang='fr') ))
g.add( (schema , DC.title, Literal(schema_title_en, lang='en') ))


# metadata
g.add( (schema , DCTERMS.creator,     URIRef(schema_creator)    )) 
g.add( (schema , DCTERMS.contributor, URIRef(schema_contributor))) 
g.add( (schema , DCTERMS.publisher,   URIRef(schema_creator)  ))
g.add( (schema , DCTERMS.publisher,   URIRef(schema_contributor)  ))

g.add( (schema , DCTERMS.created,  Literal(schema_created, datatype=XSD.date)) )
g.add( (schema , DCTERMS.isssued,  Literal(schema_created, datatype=XSD.date)) )
g.add( (schema , DCTERMS.modified, Literal(schema_modified, datatype=XSD.date)) )

g.add( (schema , DCTERMS.license , URIRef(schema_license) )) 
g.add( (schema , DCTERMS.accessRights, URIRef(schema_access) )) 

g.add( (schema , VOID.sparqlEndpoint, URIRef(sparql_endpoint) ))
g.add( (schema , VOID.uriSpace , URIRef(agrist_ns) ))

g.add( (schema , DCAT.version , Literal(schema_version) ))


# In[77]:


print(g.serialize(format="turtle").decode('utf-8'))


# In[78]:


serialize_Graph(g, agrist_ttl)


# #### define top concepts (categories)

# In[79]:


g = new_Graph(agrist_ns)

for ind, row in agrist_df.drop_duplicates(subset=['category','category-label-fr']).iterrows():

    sector = URIRef(agrist_ns + row['sector'])
    lbl_fr   = Literal(row['sector-label-fr'], lang='fr') 

    g.add( (sector , RDF.type, SKOS.Concept ))
    g.add( (sector , SKOS.topConceptOf, schema ))
    g.add( (sector , SKOS.prefLabel,  lbl_fr))

    
    category = URIRef(agrist_ns + row['category'])
    lbl_fr   = Literal(row['category-label-fr'], lang='fr')
    
    g.add( (category , RDF.type, SKOS.Concept ))
    #g.add( (category , SKOS.topConceptOf, schema ))
    g.add( (category , SKOS.prefLabel,  lbl_fr))


# In[80]:


print(g.serialize(format="turtle").decode('utf-8'))


# In[81]:


serialize_Graph(g, agrist_ttl, append=True)


# #### define all concepts (sub-categories) 

# In[82]:


g = new_Graph(agrist_ns)
for ind, row in agrist_df.iterrows():
    
    if len(row['sub-category']) > 0:
    
        category = URIRef(agrist_ns + row['category'])
        sub_category = URIRef(agrist_ns + row['sub-category'])
        lbl_fr   = Literal(row['sub-category-label-fr'], lang='fr')
        editorial_note   = Literal(row['editorialNote'], lang='fr')

        g.add( (sub_category , RDF.type, SKOS.Concept ))
        g.add( (sub_category , SKOS.broader, category ))
        g.add( (sub_category , SKOS.prefLabel,  lbl_fr))
        g.add( (sub_category , SKOS.editorialNote,  editorial_note))
    else:
        category = URIRef(agrist_ns + row['category'])
        editorial_note   = Literal(row['editorialNote'], lang='fr')
        g.add( (category , SKOS.editorialNote,  editorial_note))


# In[83]:


print(g.serialize(format="turtle").decode('utf-8'))


# In[84]:


serialize_Graph(g, agrist_ttl, append=True)


# In[ ]:




