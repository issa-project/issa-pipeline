#!/usr/bin/env python
# coding: utf-8

# # ISSA-2: convert the AgrIST-Thema thesaurus from the Excel to RDF 
# 
# Note: *rdflib* does not output the triples in the order they are added, we slightly modify the serialization from a straight forward way. 

# In[32]:


import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDF, SKOS, RDFS, DCTERMS, XSD, VOID, DCAT
import datetime
import re


# In[33]:


agrist_fn = 'Plan de catégorisation AgrIST-Thema-20230523.xlsx'
agrist_df = pd.read_excel(agrist_fn, 0, 
                          usecols='A:H',
                          names=['category',  'category-label-fr', 'category-label-en',
                                 'sub-category', 'sub-category-label-fr', 'sub-category-label-en',
                                 'scopeNote', 'editorialNote'],
                          index_col=None)

schema_title_en = u'AgrIST-Thema categorization scheme'
schema_title_fr = u'Plan de catégorisation AgrIST-Thema'

# this comment is needed to put the rdfs prefix as early as posible 
schema_comment = u'Plan de catégorisation utlisé dans Agritrop (version du 23 mai 2023)'

schema_creator     = 'https://ror.org/05kpkpg04' #CIRAD
schema_contributor = 'https://ror.org/02kvxyf05' #INRIA

schema_version = '2023.05.23'
schema_created = '2023-06-29'
schema_issued  = '2023-06-29'
schema_modified = datetime.datetime.now().strftime('%Y-%m-%d')

schema_license = 'https://creativecommons.org/licenses/by-nc/4.0/'
schema_access =  'http://purl.org/eprint/accessRights/OpenAccess'

sparql_endpoint = 'https://data-issa.cirad.fr/sparql'

agrist_ttl = 'AgrIST-Thema-v20230523.ttl'
agrist_ns = 'http://agrist.cirad.fr/agrist-thema/'
agrist_schema = agrist_ns


# In[34]:


agrist_df['category'] = agrist_df['category'].fillna(method='ffill')
agrist_df['category-label-fr'] = agrist_df['category-label-fr'].fillna(method='ffill')
agrist_df['category-label-en'] = agrist_df['category-label-en'].fillna(method='ffill')
agrist_df = agrist_df.dropna(subset='sub-category').apply(lambda x: x.str.strip()).fillna('')
#agrist_df['category'] = agrist_df['sub-category'].str[0]


# In[35]:


agrist_df


# #### start the graph with namespaces

# In[36]:


def new_Graph(agrist_ns = 'https://agrist.cirad.fr/'):
    g = Graph()

    g.bind('skos', SKOS)
    g.bind('dc', DC)
    g.bind('dct', DCTERMS)
    g.bind('rdfs', RDFS)
    g.bind('dcat', DCAT)
    g.bind('void', VOID)
    g.bind('agrist-thema', Namespace(agrist_ns))
    
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

# In[37]:


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


# In[38]:


serialize_Graph(g, agrist_ttl)


# #### define top concepts (categories)

# In[39]:


g = new_Graph(agrist_ns)
for ind, row in agrist_df.drop_duplicates(subset=['category','category-label-fr','category-label-en']).iterrows():
    
    category = URIRef(agrist_ns + row['category'])
    lbl_fr   = Literal(row['category-label-fr'], lang='fr')
    lbl_en   = Literal(row['category-label-en'], lang='en')
    
    g.add( (category , RDF.type, SKOS.Concept ))
    g.add( (category , SKOS.topConceptOf, schema ))
    g.add( (category , SKOS.prefLabel,  lbl_fr))
    g.add( (category , SKOS.prefLabel,  lbl_en))


# In[40]:


print(g.serialize(format="turtle").decode('utf-8'))


# In[41]:


serialize_Graph(g, agrist_ttl, append=True)


# #### define all concepts (sub-categories) 

# In[42]:


g = new_Graph(agrist_ns)
for ind, row in agrist_df.iterrows():
    
    category = URIRef(agrist_ns + row['category'])
    sub_category = URIRef(agrist_ns + row['sub-category'])
    lbl_fr   = Literal(row['sub-category-label-fr'], lang='fr')
    lbl_en   = Literal(row['sub-category-label-en'], lang='en')
    
    g.add( (sub_category , RDF.type, SKOS.Concept ))
    g.add( (sub_category , SKOS.broader, category ))
    g.add( (sub_category , SKOS.prefLabel,  lbl_fr))
    g.add( (sub_category , SKOS.prefLabel,  lbl_en))


# In[43]:


print(g.serialize(format="turtle").decode('utf-8'))


# #### add scopeNotes

# In[44]:


for ind, row in agrist_df.iterrows():
    
    sub_category = URIRef(agrist_ns + row['sub-category'])
    scope_note   = Literal(row['scopeNote'], lang='fr')
    editorial_note = Literal(row['editorialNote'], lang='fr')
    
    g.add( (sub_category , SKOS.scopeNote,  scope_note))
    g.add( (sub_category , SKOS.editorialNote,  editorial_note))


# #### add seeAlso

# In[45]:


agrist_df['editorialNotes'] = agrist_df['editorialNote'].apply(lambda x: x.split('\n'))

agrist_df = agrist_df.explode('editorialNotes')


# In[46]:


sub_categories_codes = sorted(agrist_df['sub-category'].unique())
categories_codes = sorted(agrist_df['sub-category'].apply(lambda x: x[0]).unique())

def expand_range(codes):
    code_range = codes.split('-')
    expanded_range = [sub_categories_codes[x] for x  in range(sub_categories_codes.index(code_range[0]),
                                                              sub_categories_codes.index(code_range[1])+1) ]

    return expanded_range

def range_is_category(code_range):
    category = code_range[0][0]
    category_range = [x for x in sub_categories_codes if x.startswith(category)]
    if len(code_range) == len(category_range):
        return category
    return code_range

def expand_codes(codes):
    if '-' in codes:
        return range_is_category(expand_range(codes))
    elif ',' in codes:
        return list(map(str.strip, codes.split(',')))
    elif 'les codes' in codes:
        return re.findall(r'\b[A-Z]\b', codes)
    return [codes]

def validate_code(code):
    return code if code in sub_categories_codes + categories_codes else ''


# In[47]:


s = 'les codes E'
re.findall(r'\b[A-Z]\b', s)


# In[48]:


agrist_df['seeAlso'] = agrist_df['editorialNotes'].apply(lambda x: x.split(' voir ')[-1].strip() ) 
agrist_df['seeAlso'] = agrist_df['seeAlso'].apply(expand_codes) 

agrist_df = agrist_df.explode('seeAlso')
agrist_df['seeAlso'] = agrist_df['seeAlso'].apply(validate_code)


# In[49]:


agrist_df.tail()


# In[50]:


for ind, row in agrist_df.iterrows():

    if row['seeAlso']:
        sub_category = URIRef(agrist_ns + row['sub-category'])
        see_also     = URIRef(agrist_ns + row['seeAlso'])

        g.add( (sub_category , RDFS.seeAlso, see_also ))


# In[51]:


print(g.serialize(format='turtle').decode("utf-8"))


# In[52]:


serialize_Graph(g, agrist_ttl, append=True)


# In[ ]:




