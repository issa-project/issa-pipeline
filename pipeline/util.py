# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""
import os
import datetime
import logging
from copy import deepcopy

import sys

#%%
def always_log_exceptions(exctype, value, tb):
    
    #read last element in hope that this is the one we need
    #TODO:refactor
    logger=[logging.getLogger(name) for name in logging.root.manager.loggerDict][-1]
    
    logger.exception('Uncaught exception', exc_info=(exctype, value, tb))
    
    
#%%
def open_timestamp_logger(log_prefix=None, 
                          log_dir=None, 
                          first_line=None, 
                          console_level=logging.INFO,
                          file_level=logging.DEBUG):
    
    logger = logging.getLogger(log_prefix)
    logger.setLevel(file_level)
    
    # remove all previously created streams to begin a new ones 
    if logger.hasHandlers():
        for i in range(len(logger.handlers)-1, -1, -1) :
            handler = logger.handlers[i]
            handler.close()
            logger.removeHandler(handler)
    
    # create console handler with a higher log level
    console = logging.StreamHandler()
    console.setLevel(console_level)
    logger.addHandler(console)
    
    # create log dir
    if log_dir is not None:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    # create file handler with lower log level
    if log_prefix is not None:
        fname = '%s_%s.log' % (log_prefix, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        log_file = logging.FileHandler(os.path.join(log_dir, fname) )
        log_file.setLevel(file_level)
        log_file.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%d/%m/%Y %H:%M:%S'))
        logger.addHandler(log_file)

    # output a line
    if first_line is not None:
        logger.info(first_line)
        
    sys.excepthook=always_log_exceptions
        
    return logger

def close_timestamp_logger(logger):
    logging.shutdown()
    
#%%
import ast
import pandas as pd

def read_metadata(filePath):
    """
    Read raw or processed metadata file converting columns into lists when
    nesessary

    """
    df = pd.read_csv(filePath, sep='\t', encoding='utf-8')
    #df = pd.read_csv(filePath, sep='\t', encoding='utf-8', 
    #                 doublequote=False, escapechar="\\" )
    
    for col in df.columns:
        try:
            #convert some columns to lists
            df[col] = df[col].apply(ast.literal_eval)
        except: 
            pass

    return df

def save_metadata(df, filePath):
    """
    Save processed DataFrame to a TSV file

    """
    if filePath is not None: 
        
        if not os.path.exists(os.path.dirname(filePath)):
            os.makedirs(os.path.dirname(filePath))
            
        df.to_csv(filePath, sep='\t', encoding='utf-8', index=False)
        #df.to_csv(filePath, sep='\t', encoding='utf-8', index=False,
        #          doublequote=False, escapechar="\\" )
    
    return df

#%%
import json
def read_paper_json(json_path):
    json_path = os.path.realpath(os.path.normpath(json_path))
    with open(json_path, 'r' , encoding='utf-8', errors='ignore' ) as json_file:
            json_dict = json.load(json_file)
            
    return json_dict

def save_paper_json(json_path, json_dict): 
    json_path = os.path.realpath(os.path.normpath(json_path))
    
    with open(json_path, 'w' , encoding='utf-8') as json_file:
                json.dump(json_dict, json_file, indent=4, ensure_ascii=False)    
                
                
#%%
import shutil

def copy_file(file_path, to_folder ):

    dest_file_path = os.path.join(to_folder, os.path.basename(file_path))
    shutil.copyfile(file_path, dest_file_path)  
    
    return dest_file_path

def _remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    #os.chmod(path, stat.S_IWRITE)
    func(path)
    
#%%
try:
    import pycld2 as cld2
except:
    # Fake it on Windows
    class cld2(object):
        def detect(text, hintLanguage=None, bestEffort=False):
            isReliable = True
            textBytesFound = len(text)
            details = (('ENGLISH', 'en', 99, 100.0), ('Unknown', 'un', 0, 0.0), ('Unknown', 'un', 0, 0.0) )
            return isReliable, textBytesFound, details
    

def detect_lang(text, hint_language=None, best_effort=False,
                all_details=False, return_score=False,
                logger=None):
    """
    Detect language of the text using pycld2 

    Parameters
    ----------
    text : string
        Text to detect language for.
    all_details : bool, optional
        If True and more thaan one language is detetced return all of the
        languages separated by comma. 
        If False alsways return the first detected language  The default is False.
    logger: logging.Logger, optional 
        If specified then the details of language detection will be logged. 
        The defaoult is None
        
    Returns
    -------
    lang : str or None
        If detection is reliable then return string of detected language code 
        in ISO 639-1 format.

    """
    
    isReliable, textBytesFound, details = cld2.detect(text, hintLanguage=hint_language)
    
    #isReliable, textBytesFound, details = (True, len(text), (('ENGLISH', 'en', 99, 1157.0), ('Unknown', 'un', 0, 0.0), ('Unknown', 'un', 0, 0.0)))
    
    if logger:
        logger.debug(text[:500])
        logger.debug(details)
 
    if not isReliable and best_effort:   
        isReliable, textBytesFound, details = cld2.detect(text, hintLanguage=hint_language, bestEffort=True)
        if logger:
            logger.debug('best effort')
            logger.debug(details)
 
    lang=None
    score=None
    
    if isReliable:
        lang = details[0][1]
        score = details[0][2]/100.0
        
        #typically the first language is good enough to return if more details
        #are needed use the details parameter
        if all_details and details[1][2] > 0:
            lang = ','.join([lang, details[1][1], details[2][1]])
            
    
    if return_score:
        return  lang , score
    else:
        return lang

#%%
def get_nested_dict_value(nested_dict, path_list, default=None):
    """
    FEtch the value from a dictionary provided the path as list of strings 
    and indecies

    Parameters
    ----------
    nested_dict : dict

    path_list : list
        list of list of strings and/or indecies

    Returns
    -------
    value : any type
    """
    
    try:
        
        value = nested_dict
        for k in path_list:
            value = value[k] 
            
    except KeyError:
        if  default is not None:
            value=default
        else:
            raise 
            
        
    return value
    
def set_nested_dict_value(nested_dict, path_list, value):
    """
    Assign value to a key mapped by path as list of strings and indices.
    Creates list if an index in a path os 0 but nested value is empty.
    In other cases if index is out of range then exception will be thrown.

    Parameters
    ----------
    nested_dict : dict

    path_list : list 
        list of list of strings and/or indices

    value : any type
        value to assign
    Returns
    -------
    nested_dict : dict
        updated dictionary

    """

    d = nested_dict
    for k in path_list[:-1]:
        if k == 0 and len(d) == 0:
            # create list for index=0 if list does not exist
            d = []
        d = d[k] 
    
    d[path_list[-1]] = value 
    
    return nested_dict    

# inspired by post  
# https://gist.github.com/angstwad/bf22d1822c38a92ec0a9?permalink_comment_id=4038517#gistcomment-4038517
def merge_nested_dicts(dict_a: dict, dict_b: dict):
    """
    Recursively merge nested dictionaries. The values of the second dictionary
    will overwrite the values for the same key in first dictionary. 

    Parameters
    ----------
    dict_a : dict
    dict_b : dict

    Returns
    -------
    result : dict
         merged dictionary
    """
    result = deepcopy(dict_a)
    for bk, bv in dict_b.items():
        av = result.get(bk)
        if isinstance(av, dict) and isinstance(bv, dict):
            result[bk] = merge_nested_dicts(av, bv)
        else:
            result[bk] = deepcopy(bv)
    return result

#%% 
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
    
