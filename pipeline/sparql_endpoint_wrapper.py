# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""
import pandas as pd
import json

from retrying import retry
from SPARQLWrapper import SPARQLWrapper, JSON #, DIGEST, TURTLE, N3, XML, JSONLD, 

            
class SPARQL_Endpoint_Wrapper(object):
    def __init__(self, endpoint='http://localhost/sparql',
                       timeout=0):
		#TODO: add languages support
        self.sparql_wrapper = SPARQLWrapper(endpoint)
        self.sparql_wrapper.addParameter('timeout', str(timeout))

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
    
