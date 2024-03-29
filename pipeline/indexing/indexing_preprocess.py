# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 20:52:23 2022

@author: abobashe
"""

import os
import sys
import glob

sys.path.append('..')  
from util import read_paper_json
from util import open_timestamp_logger, close_timestamp_logger
from util import get_nested_dict_value
from util import add_path_to_config

add_path_to_config()
from config import cfg_indexing_preprocess as cfg

#%% Set up logging
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               first_line = 'Preprocessing text for Annif indexing...')
#%% Helper functions
def get_language(json_dict):
    """
    Determine the language of the document because each language has its particular
    Annif indexing model
    Parameters:
        json_dict (dict): json dictionary with metadata and text
    Returns:
        lang (str): language of the document
    """
    lang=''
    for part in cfg.LANGUAGE_DETERMINERS:
        text = get_nested_dict_value(json_dict, cfg.JSON_TEXT_MAP[part][0] , default='')
        lang = get_nested_dict_value(json_dict, cfg.JSON_TEXT_MAP[part][1] , default='unk')
        #logger.debug('%s: %s , %r' % (part, lang, (lang in cfg.OUTPUT_LANG)) )
        if text and (lang in cfg.OUTPUT_LANG):
            break
    
    if not lang:
        raise UserWarning('cannot determine the language')       
        
    if lang not in cfg.OUTPUT_LANG:
        raise UserWarning('text in  %s cannot be indexed %s' % (lang, part))

    return lang
       
def preprocess_one(f_json, f_txt):
    """
    Get text from json representation and save it to a text file

    Parameters:
        f_json (str): path to json file
        f_txt (str): path to output text file

    Returns:
        f_txt (str): path to output text file    
    """
    try:
        paper_json =  read_paper_json(f_json)
        
        lang= get_language(paper_json)
        
        text = cfg.PARTS_SEPARATOR.join( [ get_nested_dict_value(paper_json, v[0]) 
                                           for k,v in cfg.JSON_TEXT_MAP.items() 
                                           if get_nested_dict_value(paper_json, v[1], default='unk') == lang] ) 
        text = text.strip()
            
        #change the file extension to indicate the language
        f_txt = f_txt.replace('lang', lang )
        
        with open(f_txt, 'w',  encoding='utf-8') as txt_file:
                txt_file.write(text)
        
    except Exception as e:
        logger.exception(e)

    return f_txt

def preprocess_json_to_text():
    """
    Loop through documents' json representation and save it to text files

    """

    files = glob.glob(os.path.join(cfg.INPUT_PATH, cfg.INPUT_PATTERN))
    logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 

     
    for f_json in files:
        logger.info(f_json + '--->')
        
        filename = os.path.basename(f_json).split('.')[0]
        f_txt = os.path.join(cfg.OUTPUT_PATH, 'lang',  filename + cfg.OUTPUT_SUFFIX)  

        f_txt = preprocess_one(f_json, f_txt)
        logger.info(f_txt)
    
    return

def create_lang_dirs():
    """
    Make directories for training data according to the config

    """
    for lang in cfg.OUTPUT_LANG:
       os.makedirs(os.path.join(cfg.OUTPUT_PATH, lang), exist_ok=True)

#%%  Main
if __name__ == '__main__':
    if cfg.DO_INDEX:
        create_lang_dirs()
        preprocess_json_to_text()
    else:
        logger.info('Indexing is turned off. Set DO_INDEX to True in the config file to enable indexing.')

        
close_timestamp_logger(logger)