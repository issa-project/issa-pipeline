# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 20:52:23 2022

@author: abobashe
"""

import os
import sys
import glob

sys.path.append('..')  

from config import cfg_indexing_preprocess as cfg
from util import read_paper_json
from util import open_timestamp_logger, close_timestamp_logger
from util import get_nested_dict_value

#%% 
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               first_line = 'Preprocessing text for Annif indexing...')
#%%
def create_lang_dirs():
    """
    Make directories for training data according to the config

    """
    for lang in cfg.OUTPUT_LANG:
       os.makedirs(os.path.join(cfg.OUTPUT_PATH, lang), exist_ok=True)
       
#%%
def get_language(json_dict):
    """
    Determine the language of the document because each language has its own models

    """
    lang=''
    for part in cfg.LANGUAGE_DETERMINATORS:
        lang = get_nested_dict_value(json_dict, cfg.JSON_TEXT_MAP[part][1] )
        #logger.debug('%s: %s , %r' % (part, lang, (lang in cfg.OUTPUT_LANG)) )
        if lang in cfg.OUTPUT_LANG:
            break
    
    if not lang:
        raise UserWarning('cannot determine the language')       
        
    if lang not in cfg.OUTPUT_LANG:
        raise UserWarning('text in  %s cannot be indexed %s' % (lang, part))

    return lang
       
#%%
def preprocess_one(f_json, f_txt):
    try:
        #paper_id = os.path.basename(f_json).split('.')[0]
        
        #read document json
        #paper_json_path = glob.glob(os.path.join(cfg.INPUT_JSON_PATH,  paper_id + '*.json'))
        
        #if ( not paper_json_path):
       ##
       #return

        #paper_json =  read_paper_json(paper_json_path[0])
        
        #text = cfg.PARTS_SEPARATOR.join( [ get_nested_dict_value(paper_json, v) for k,v in cfg.JSON_TEXT_MAP.items()] ) 
        paper_json =  read_paper_json(f_json)
        
        lang= get_language(paper_json)
        
        text = cfg.PARTS_SEPARATOR.join( [ get_nested_dict_value(paper_json, v[0]) 
                                           for k,v in cfg.JSON_TEXT_MAP.items() 
                                           if get_nested_dict_value(paper_json, v[1]) == lang] ) 
        text = text.strip()
            
        #change the file extension to indicate the language
        f_txt = f_txt.replace('lang', lang )
        
        with open(f_txt, 'w',  encoding='utf-8') as txt_file:
                txt_file.write(text)
        
    except Exception as e:
        logger.exception(e)

    return f_txt

def preprocess_json_to_text():
     #files = glob.fnmatch.filter(os.listdir(json_path), cfg.INPUT_PATTERN)
     #logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 
     
     files = glob.glob(os.path.join(cfg.INPUT_PATH, cfg.INPUT_PATTERN))
     logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 

     
     for f_json in files:
         #f_json = os.path.join(json_path, f_json)
         #f_json = os.path.realpath(os.path.normpath(f_json))
         logger.info(f_json + '--->')
         
         filename = os.path.basename(f_json).split('.')[0]
         f_txt = os.path.join(cfg.OUTPUT_PATH, 'lang',  filename + cfg.OUTPUT_SUFFIX)  
         
         #f_txt = os.path.join(txt_path, os.path.basename(f_json).split('.')[0] + cfg.OUTPUT_SUFFIX) #TODO: add or replace 
         #f_txt = os.path.realpath(os.path.normpath(f_txt))

         f_txt = preprocess_one(f_json, f_txt)
         logger.info(f_txt)
    
     return


#%%     
if __name__ == '__main__':
    create_lang_dirs()
        
    preprocess_json_to_text()
        
close_timestamp_logger(logger)