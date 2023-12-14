# -*- coding: utf-8 -*-
""" 
Document corpus metadata processing functions

This script contains functions to process metadata in TSV or CSV files.

Created on Wed June  21 16:35:35 2023

@author: abobashe
"""
import os
import sys
import pandas as pd
import numpy as np
from typing import Union
import re
from langdetect import detect_langs , DetectorFactory

sys.path.append('..') 
from util import read_metadata, save_metadata
from util import open_timestamp_logger, close_timestamp_logger, INFO, DEBUG
from util import detect_lang
from util import add_path_to_config  

add_path_to_config()
from config import cfg_process_corpus_metadata as cfg

#%% Set up logging
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               file_level=DEBUG if cfg.DEBUG else INFO,
                               first_line = 'Processing %s metadata file...' % cfg.RAW_DATA_FILENAME)

#%% String or list manipulation functions

# These functions are used to process the metadata in pandas DataFrame.
# The functions are applied to a pandas DataFrame columns using the apply() method.
# They can be applied to a single string or a list of strings.
# The output is a single string or a list of strings.

def to_capital(x:Union[str, list])->Union[str, list]:  
    """Convert a string or a list of strings to capital case.
    
    Parameters:
      x: string or list of strings
    
    Returns:
         string  or list of strings
    """      
    if isinstance(x, str): 
        return x.title()
    elif isinstance(x, list):
        return [_x.title for _x in x]
    return x 

def to_lower(x:Union[str, list])->Union[str, list]:      
    """
    Convert a string or a list of strings to lower case.
    
    Parameters:
      x: string or list of strings
    
    Returns:
         string  or list of strings
    """  
    if isinstance(x, str): 
        return x.lower()
    elif isinstance(x, list):
        return [_x.lower() for _x in x]
    return x 

def to_upper(x:Union[str, list])->Union[str, list]:
    """
    Convert a string or a list of strings to upper case.    

    Parameters:
        x: string or list of strings
    Returns:
        string  or list of strings
    """        
    if isinstance(x, str): 
        return x.upper()
    elif isinstance(x, list):
        return [_x.upper() for _x in x]
    return x 

def extract_string(x:Union[str, list], regex:str, group=0, default='')->Union[str, list]:  
    """ 
    Extract a string from a larger string or a list of strings using a regular expression pattern.

    Parameters:
        x: string or list of strings
        regex: regular expression pattern to match 
        group: group number to return (default: 0) 
        default: default value if no match is found (default: empty string)

    Returns:
        string  or list of strings
    """ 
    def _extract_string(x:str, regex:str, group:int, default)->str:
        match = re.search(regex,  str(x))
        return match.group(group) if match else default
    
    if isinstance(x, str): 
        return _extract_string(x, regex, group, default)
    elif isinstance(x, list):
        return [_xx for _xx in [_extract_string(_x, regex, group, default) for _x in x] if _xx != default]
        #return [_extract_string(_x, regex, group, default) for _x in x] 
    return x 

def map_to_value(x:Union[str, list], map:dict , default=None)->Union[str, list]: 
    """ 
    Map a string or a list of strings to a value(s) based on a dictionary.

    Parameters:
        x: string or list of strings
        map: dictionary to map values
        default: default value if no match is found (default: None)

    Returns:
        string  or list of strings
    """
        
    if isinstance(x, str): 
        return map.get(x , map.get('default', default))
    elif isinstance(x, list):
        return [ map.get(_x , map.get('default', default)) for _x in x]
    return x 

# function that maps a column to a value based on a SPARQL query
def map_to_value_sparql(x:Union[str, list], sparql_endpoint, sparql_query:str, 
                        input='label', language='en')->Union[str, list]:  
    """
    Map a string or a list of strings to a value(s) based on a SPARQL query.

    Parameters:
        x: string or list of strings
        sparql_endpoint: SPARQL endpoint
        sparql_query: SPARQL query template where %s is replaced with the values from x
        input: type of input values 'label' or 'uri'  (default: 'label')
        language: language of input labels (default: 'en')
        
    Returns:
        string  or list of strings of mapped labels if the input is a list of uris 
        or mapped uris if the input is a list of labels 
    """
    
    if isinstance(x, str): 
        x = [x]

    if isinstance(x, list) and len(x) > 0:
        if input == 'label':
            vars = ['("%s"@%s)' % (_x, language) for _x in x]
            query = sparql_query % (' '.join(vars) )  

        elif input == 'uri':   
            vars = ['(<%s>)' % _x for _x in x]
            query = sparql_query % (' '.join(vars) , language )

        else:
            raise ValueError('input must be either "label" or "uri"')   


        #query = replace(query, r'\s+', ' ') 
        
        res = sparql_endpoint.sparql_to_dataframe(query)

        # preserve original order
        res_dict = dict(zip(res.iloc[:, 0], res.iloc[:, 1]))

        return [res_dict.get(_x, '') for _x in x]
    
    return x

def expand_prefix(x:Union[str, list], prefix_map:dict)->Union[str, list]:
    """
    Expand a string or a list of strings with a given RDF prefix map.

    Parameters:
        x: string or list of strings with prefixes
        prefix_map: dictionary of prefix-value pairs

    Returns:
        string  or list of strings
    """
    def _expand_prefix_str(x:str, prefix_map:dict)->str:
        for k,v in prefix_map.items():
            if x.startswith(k):
                return v + x[len(k)+1:]
        return x
    
    if isinstance(x, str): 
        return _expand_prefix_str(x, prefix_map)
    elif isinstance(x, list):
        return [_expand_prefix_str(_x, prefix_map) for _x in x]
    return x


def replace(x:Union[str, list,dict], pattern, repl='')->Union[str, list, dict]:   
    """
    Replace a substring in a string or a list of strings.

    Parameters:
        x: string or list of strings or dictionary of strings
        pattern: regular expression pattern to substitute in an input string
        repl: replacement string (default: '')

    Returns:
        string  or list of strings
    """ 
    if isinstance(x, str): 
        return re.sub(pattern, repl, x)
    elif isinstance(x, list):
        return [re.sub(pattern, repl, _x) for _x in x]
    elif isinstance(x, dict):     
        return {k:re.sub(pattern, repl, v) for k,v in x.items()}
    return x 

def prepend(x:Union[str, list], prefix:str)->Union[str, list]:
    """
    Prepend a string or a list of strings with a given prefix.

    Parameters:
        x: string or list of strings
        prefix: string to prepend

    Returns:
        string  or list of strings
    """
    if isinstance(x, str): 
        return prefix + x
    elif isinstance(x, list):
        return [prefix + _x for _x in x]
    return x

#%% List only manipulation functions.

# These functions take a list as an input and return a list as an output

def remove_from_list(dl:list, pattern:str)->list:
    """ 
    Remove elements from a list that match a given pattern.

    Parameters:
        dl: list of strings
        pattern: regular expression pattern to match

    Returns:
        list of strings
    """

    if isinstance(dl, list):
        return list(filter(lambda x: x and not re.search(pattern, x)  , dl))
    return dl

def keep_in_list(dl:list, pattern:str)->list:
    """     
    Keep strings in a list of strings only if they match a given pattern.
        
    Parameters:
        dl: list of strings
        pattern: regular expression pattern to match
  
    Returns:
        list of strings
    """
    if isinstance(dl, list):
        return list(filter(lambda x: x and re.search(pattern, x)  , dl))
    return dl


def take_at(dl:list, index=0, default='')->str:
    """
    Take an element from a list at a given index.
    If the index is negative, the element is taken from the end of the list.
 
    Parameters:
        dl: list of strings
        index: index of the element to take
        default: default value if the index is out of bounds (default: empty string)

    Returns:
        string
    """
    if not isinstance(dl, list):
        return default
    
    if index >= 0:
        return dl[index] if len(dl) > index else default
    else:
        return dl[index] if len(dl) > abs(index)-1 else default
    

def take_first(dl:list, default='')->str:
    """ 
    Convenience function to take the first element from a list of strings. 
    
    Parameters:
        dl: list of strings
        default: default value if a list is empty (default: empty string)
            
    Returns:
        string
    """
    return take_at(dl, 0, default)

def take_last(dl:list, default='')->str:
    """ 
    Convenience function to take the last element from a list of strings. 
    
    Parameters:
        dl: list of strings
        default: default value if a list is empty (default: empty string)
            
    Returns:
        string
    """
    return dl[-1] if len(dl) > 0 else default

def concatenate(dl:list, sep=',', default='')->str:
    """
    Concatenate a list of strings into a single string using a given separator.

    Parameters:
        dl: list of strings
        sep: separator (default: ',')
        default: default value if the input is not a list (default: empty string)

    Returns:
        string of concatenated strings
    """ 
    if not isinstance(dl, list):
        return default
    return sep.join(dl)


#%% Language detection functions

# These functions are used to detect the language of a string
# Two methods are used: langdetect and pycld2 (pycld2 is more accurate but slower and is not supported on Windows)

DetectorFactory.seed = 42
def detect_lang_langdetect(text:str, default='')->pd.Series:
    """
    Detect language of a string using langdetect package.

    Parameters:
        text: string to detect language for
        default: default language if detection fails (default: '')

    Returns:
        pandas Series with detected language and probability score
    """
    try:
        langs = detect_langs(text)
        return pd.Series([langs[0].lang, langs[0].prob] )
    except:
        return pd.Series([default, 0.0 ])
    
def detect_lang_cld2(text:str, hint=None, default=''):
    """
    Detect language of a string using pycld2 package.

    Parameters:
        text: string to detect language for
        hint: language hint (default: None)
        default: default language if detection fails (default: '')

    Returns:    
        pandas Series with detected language and probability score
    """
    hint = hint if hint != 'en' else None
    bf = cfg.BEST_EFFORT_LANG_DETECTION
    try: 
        lang, score = detect_lang(text, 
                                best_effort=bf, hint_language=hint, 
                                return_score=True, logger=logger )
        return pd.Series([lang, score])
    except:
        return pd.Series([default, 0.0 ])

def detect_language(text:Union[str, list], hint=None, default='')->pd.Series: 
    """
    Detect language of a string using a method defined in the config.

    Parameters:

        text: string or list of strings to detect language for
        hint: language hint (default: None)
        default: default language if detection fails (default: '')

    Returns:
        pandas Series with detected language and probability score
    """

    if isinstance(text, str):
        if cfg.LANG_DETECTION_METHOD == 'cld2': 
            return detect_lang_cld2(text, hint, default)
        
        elif cfg.LANG_DETECTION_METHOD == 'langdetect':
            return detect_lang_langdetect(text, default)
        
        return pd.Series([default, 0.0 ])
    
    if isinstance(text, list):
        if cfg.LANG_DETECTION_METHOD == 'cld2': 
            list_of_series = [detect_lang_cld2(x, hint, default) for x in text]
        
        elif cfg.LANG_DETECTION_METHOD == 'langdetect':
            list_of_series = [detect_lang_langdetect(x, default) for x in text]
            
        else:
            return pd.Series ([default] * len(text)), [0.0] * len(text)
           
        return pd.Series([ [x[0] for x in list_of_series], [x[1] for x in list_of_series] ] )

    return pd.Series([default, 0.0 ])

#%% Dataset specific manipulation functions

# These functions are used to manipulate the DataFrame with the dataset
# The functions are applied to a pandas DataFrame rows using the apply() method.

# def select_text_by_lang(row:pd.Series, textPart: Union['abstract', 'title'], doc_lang_column='language')->pd.Series:
#     """
#     Select the text in a given language from a list of texts in different languages according to the language of the document.

#     Parameters:
#         row: pandas Series with the row to process
#         textPart: text part to process (abstract or title)
#         base: column name with the language of the document (default: 'language')

#     Returns:
#         pandas Series with the selected text and language
#     """

#     doc_lang = row[doc_lang_column]
#     part_text_list = row[f'{textPart}s'] if isinstance(row[f'{textPart}s'], list) else []
#     part_lang_list = row[f'{textPart}s_lang'] if isinstance(row[f'{textPart}s_lang'], list) else []

#     # zip lists into dictionary for easier access
#     part_text_dict = dict(zip(part_lang_list, part_text_list))

#     if part_text_dict and isinstance(part_text_dict, dict):
#         if doc_lang in part_text_dict.keys():
#             row[f'{textPart}'] = part_text_dict[doc_lang]
#             row[f'{textPart}_lang'] = doc_lang
#         elif len(part_text_dict) > 0:
#             row[f'{textPart}'] = list(part_text_dict.values())[0]
#             row[f'{textPart}_lang'] = list(part_text_dict.keys())[0]
#         else:
#             row[f'{textPart}'] = ''
#             row[f'{textPart}_lang'] = ''

#     return row 

# def map_to_value_sparql_by_lang(row:pd.Series, sparql_endpoint, sparql_query:str,
#                                       input_column:str, output_column:str,
#                                       doc_lang_column='language' )->pd.Series:

#     row[output_column] = map_to_value_sparql(row[input_column], sparql_endpoint, sparql_query,
#                                           input='uri', language=row[doc_lang_column])

#     return row






#%% Framework functions

# These functions are used to manage the calls to the data manipulation functions of the DataFrame
# The framework is based on the two configuration maps defined in the config module
# cfg.PROCESSING_MAP defines the functions to apply to the DataFrame columns and the order in which they are applied
# cfg.POST_PROCESSING_MAP defines the functions to apply to the DataFrame rows and/or the dataframe in whole and the order in which they are applied 
# The called functions can be either defined in this module or in pandas
# The parameters to the functions can be passed as a tuple or a dictionary (see call_func() function)

def call_func(pd_obj:Union[pd.Series, pd.DataFrame] , func_name, args)->Union[pd.Series, pd.DataFrame]:
    """
    Call a function on a pandas DataFrame (by row or dataframe in whole) or Series (column).

    Parameters:
        pd_obj: pandas DataFrame or Series (columns) to process
        func_name: name of the function to call 
            the function can be defined in this module or in pandas

        args: arguments to pass to the function, arguments can be passed as a tuple or a dictionary (default: None)
            if args is None, no arguments are passed to the function 
            if args is a tuple, the tuple is passed to the function as positional arguments
            if args is a dictionary, the dictionary is passed to the function as keyword arguments

    Returns: 
        pandas DataFrame or Series with the result of the function call
    """
    try:
        assert isinstance(pd_obj, (pd.Series, pd.DataFrame) )
        assert isinstance(func_name, str)
        assert isinstance(args, (tuple, dict, type(None)))   

        # check if function is defined in this module
        if func_name in globals():
            f = globals()[func_name] 

            if isinstance(args , tuple):
                return pd_obj.apply(f, args=args)
            
            elif isinstance(args , dict):
                return pd_obj.apply(f, **args)
            
            else:
                return pd_obj.apply(f)  
            
        # otherwise assume that function is defined in pandas
        else:
            f = getattr(pd_obj , func_name)
            return f(**args)
        
    except Exception as e:
        logger.error('error %s in call_func: %s, %s' % (e, func_name, args))

    return pd_obj

def process_columns(df):
    """
    Process columns in a dataframe using the functions defined in the config.PROCESSING_MAP

    Parameters:
        df: pandas DataFrame to process

    Returns:
        pandas DataFrame with processed columns
    """

    for fld, func in cfg.FIELD_PROCESSING_MAP.items():
        assert fld in df.columns,               'Field %s not found in the dataframe' % fld
        assert isinstance(func, (tuple, list)), 'Mapped value for %s must be a tuple or list' % fld 

        if isinstance(func, tuple):
            func = [func]

        for f in func:
            assert isinstance(f, tuple),                        'Mapped action for %s must be a tuple ' % fld
            assert len(f)  >= 2,                                'Mapped action for %s must be a tuple of length 2 or more' % fld
            assert isinstance(f[0], str),                       'First value of action for %s must be a function name as string'% fld
            assert isinstance(f[1], (tuple, dict, type(None))), 'Second value of action for %s must be a tuple, dict, or None' % fld
            
            # function can be either local function of this module 
            # or a function from pandas Series module
            func_name = f[0]

            # function arguments can be either tuple  or dict
            func_args = f[1] if f else None
                
            # output column can be the same as input or different
            fld_out = f[2] if len(f) > 2 else fld 

            df[fld_out] = call_func(df[fld], func_name, func_args)

            logger.info('Processed %s column with %s function' % (fld, func_name))

    return df     

#function to process dataframe from the config map
def process_dataframe(df, func_map= cfg.POST_PROCESSING_MAP ): 
    """
    Process the whole dataframe using the functions defined in the config.POST_PROCESSING_MAP

    Parameters:
        df: pandas DataFrame to process

    Returns:
        pandas DataFrame with processed columns
    """
    for step, func in func_map.items():
        
        assert isinstance(func, tuple)
        assert len(func)  >= 2
        assert isinstance(func[0], str)
        assert isinstance(func[1], (dict, type(None)))
        
        func_name = func[0]

        # function arguments have to ba a dictionary
        func_args = func[1] if func[1] else {}

        # set axis parameter to be always 1 because the default is 0 
        #func_args['axis'] =  1
               
        df = call_func(df, func_name, func_args)

        logger.info('Processed step %s calling %s function' % (step, func_name))

    return df     

def pre_process_dataframe(df):
    """
    Process dataframe row by row using the functions defined in 
    the config.PRE_PROCESSING_MAP before processing the columns

    Parameters:
        df: pandas DataFrame to process

    Returns:
        pandas DataFrame with processed columns
    """
    return process_dataframe(df, func_map= cfg.PRE_PROCESSING_MAP )     

def post_process_dataframe(df):
    """
    Process dataframe row by row using the functions defined in 
    the config.POST_PROCESSING_MAP after processing the columns

    Parameters:
        df: pandas DataFrame to process

    Returns:
        pandas DataFrame with processed columns
    """
    return process_dataframe(df, func_map= cfg.POST_PROCESSING_MAP )

#%% Processing  pipeline
def process(save_file=True):
    """
    Main function to process the metadata file from end to end.
    It reads the raw metadata file, processes the column-wise, processes the row-wise or the whole dataframe,
    and saves the processed file.
    
    Parameters:
        save_file: boolean flag to save the processed file (default: True)

    Returns:
        None
    """
    
    input_metadata_file = os.path.join(cfg.INPUT_PATH, cfg.RAW_DATA_FILENAME)
    output_metadata_file = os.path.join(cfg.OUTPUT_PATH, cfg.PROCESSED_DATA_FILENAME)

    try:
        df = read_metadata(input_metadata_file)\
            .pipe(pre_process_dataframe)\
            .pipe(process_columns)\
            .pipe(post_process_dataframe)

        if save_file:
            save_metadata(df, output_metadata_file)
            logger.info('Dataset size = %d, saved in %s' % (df.shape[0], output_metadata_file) )

    except Exception as e:
        logger.error('Error in processing metadata: %s' % e)
        raise e

#%% Main processing loop
# This is the main processing loop that is called from the command line

if __name__ == '__main__':
    process(save_file=True)

close_timestamp_logger(logger)