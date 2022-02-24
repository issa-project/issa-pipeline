# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""
import pandas as pd
import json
#import sys

from retrying import retry
#from joblib import Parallel, delayed

#sys.path.append('..')

from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE #, DIGEST, N3, XML, JSONLD, 

#from config import cfg_agrovoc_wrapper as cfg

#Emulate config
#from collections import namedtuple
#config = namedtuple('config', ['SPARQLEndpoint'])
#Agrovoc = config({'ENDPOINT': 'https://agrovoc.uniroma2.it/sparql'
#})

class cfg:
    SPARQLEndpoint = 'https://agrovoc.uniroma2.it/sparql'
    TIMEOUT = '0'
            
class Agrovoc_Wrapper(object):
    def __init__(self):
		#TODO: add languages support
        self.sparql_wrapper = SPARQLWrapper(cfg.SPARQLEndpoint)
        self.sparql_wrapper.addParameter('timeout', cfg.TIMEOUT)

#TODO: make a base class
    @retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=10, wait_random_max=2000)
    def sparql_to_dataframe(self, query):
        """
		Helper function to convert SPARQL results into a Pandas data frame.
		
		Credit to Ted Lawless https://lawlesst.github.io/notebook/sparql-dataframe.html
		"""

        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setReturnFormat(JSON)
        result = self.sparql_wrapper.query()

        processed_results = json.load(result.response)
        cols = processed_results['head']['vars']

        out = []
        for row in processed_results['results']['bindings']:
            item = []
            for c in cols:
                item.append(row.get(c, {}).get('value'))
            out.append(item)

        return pd.DataFrame(out, columns=cols)

    @retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=10, wait_random_max=2000)
    def download_vocab(self, lang, output_file):

        query = '''
                 PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
                 PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
                 CONSTRUCT
                 {
                   ?concept a skos:Concept ; 
                   ?rel ?rel_concept;   
                   skos:prefLabel ?prefLabel;
                   skos:altLabel ?altLabel . 
                 }
                 WHERE { 
                   ?concept a skos:Concept . 
                   ?concept skosxl:prefLabel/skosxl:literalForm ?prefLabel . 
                   BIND('%s' AS ?lang) 
                   FILTER(lang(?prefLabel) = ?lang) 
                   OPTIONAL{ 
                    ?concept skosxl:altLabel/skosxl:literalForm ?altLabel . 
                     FILTER(lang(?altLabel) = ?lang) 
                   } 
      
                   OPTIONAL{ 
                     VALUES ?rel { skos:broader skos:narrower skos:related } 
                     ?concept ?rel ?rel_concept .
                   } 
      
                   #?concept skos:prefLabel "citrus fruits"@en
        } 
        ''' % lang

        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setOnlyConneg(True)
        self.sparql_wrapper.setReturnFormat(TURTLE)

        result = self.sparql_wrapper.query().convert()


        with open(output_file, "wb") as text_file:
            text_file.write(result)

    @retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=10, wait_random_max=2000)
    def download_vocab_with_parent_labels(self, lang, output_file):

        query = '''
                 PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
                 PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
                 CONSTRUCT
                 {
                   ?concept a skos:Concept ; 
                   ?rel ?rel_concept;   
                   skos:prefLabel ?prefLabel;
                   skos:altLabel ?altLabel;
                   skos:altLabel ?parent_prefLabel;
                   skos:altLabel ?parent_altLabel.  
                 }
                 WHERE { 
                   ?concept a skos:Concept . 
                   ?concept skosxl:prefLabel/skosxl:literalForm ?prefLabel . 
                   BIND('%s' AS ?lang) 
                   FILTER(lang(?prefLabel) = ?lang) 
                   OPTIONAL{ 
                    ?concept skosxl:altLabel/skosxl:literalForm ?altLabel . 
                     FILTER(lang(?altLabel) = ?lang) 
                   } 
      
                   OPTIONAL{ 
                     VALUES ?rel { skos:broader skos:narrower skos:related } 
                     ?concept ?rel ?rel_concept .
                   } 

                   OPTIONAL{ 
                     ?concept skos:broader ?parent_concept .
                     ?parent_concept skosxl:prefLabel/skosxl:literalForm ?parent_prefLabel.
                     FILTER(lang(?parent_prefLabel) = ?lang) 
                   } 

                   OPTIONAL{ 
                     ?concept skos:broader ?parent_concept .
                     ?parent_concept skosxl:altLabel/skosxl:literalForm ?parent_altLabel.
                     FILTER(lang(?parent_altLabel) = ?lang)
                   } 

      
                   #?concept skos:prefLabel "citrus fruits"@en
        } 
        ''' % lang

        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setOnlyConneg(True)
        self.sparql_wrapper.setReturnFormat(TURTLE)

        result = self.sparql_wrapper.query().convert()


        with open(output_file, "wb") as text_file:
            text_file.write(result)

    @retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=10, wait_random_max=2000)
    def download_vocab_with_parent_labels_for_non_leaves(self, lang, output_file):

        query = '''
                 PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
                 PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
                 CONSTRUCT
                 {
                   ?concept a skos:Concept ; 
                   ?rel ?rel_concept;   
                   skos:prefLabel ?prefLabel;
                   skos:altLabel ?altLabel;
                   skos:altLabel ?parent_prefLabel;
                   skos:altLabel ?parent_altLabel.  
                 }
                 WHERE { 
                   ?concept a skos:Concept . 
                   ?concept skosxl:prefLabel/skosxl:literalForm ?prefLabel . 
                   BIND('%s' AS ?lang) 
                   FILTER(lang(?prefLabel) = ?lang) 
                   OPTIONAL{ 
                    ?concept skosxl:altLabel/skosxl:literalForm ?altLabel . 
                     FILTER(lang(?altLabel) = ?lang) 
                   } 
      
                   OPTIONAL{ 
                     VALUES ?rel { skos:broader skos:narrower skos:related } 
                     ?concept ?rel ?rel_concept .
                   } 

                   OPTIONAL{ 
                     ?concept skos:broader ?parent_concept .
                     ?parent_concept skosxl:prefLabel/skosxl:literalForm ?parent_prefLabel.
                     FILTER(lang(?parent_prefLabel) = ?lang)
                     FILTER EXISTS {?concept skos:narrower ?child_concept} 
                   } 

                   OPTIONAL{ 
                     ?concept skos:broader ?parent_concept .
                     ?parent_concept skosxl:altLabel/skosxl:literalForm ?parent_altLabel.
                     FILTER(lang(?parent_altLabel) = ?lang)
                     FILTER EXISTS {?concept skos:narrower ?child_concept}
                   } 

      
                   #?concept skos:prefLabel "citrus fruits"@en
        } 
        ''' % lang

        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setOnlyConneg(True)
        self.sparql_wrapper.setReturnFormat(TURTLE)

        result = self.sparql_wrapper.query().convert()


        with open(output_file, "wb") as text_file:
            text_file.write(result)


