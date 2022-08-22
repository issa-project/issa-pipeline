# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 13:52:49 2022

@author: abobashe
"""

import os
import sys
import glob
import concurrent.futures

sys.path.append('..')  

from config import cfg_annotation_agrovoc as cfg
from util import read_paper_json, save_paper_json
from util import open_timestamp_logger, close_timestamp_logger
from util import get_nested_dict_value

from wrapper_annotator import WrapperAnnotator
wa = WrapperAnnotator(concept_annotator_endpoint= cfg.PYCLINREC_ENDPOINT)

#%% 
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               first_line = 'Annotating text with Agrovoc vocabulary and pyclingrec service...')

#%%
def postprocess_pyclinrec_response(result_json):
    """
    Postprocess Spotlight response by optionally removing header and processed text, 
    also converting numnber strings to numbers.

    """    
    try:
        if cfg.REMOVE_TEXT: 
            result_json['text'] = ''

    except TypeError:
        pass    
    except KeyError:
        pass
    
    return result_json

def annotate_with_pyclinrec(f_json, f_out_json):
    """
    Send text of each part of a document to the Spotlight service that 
    returns  DBPedia NEs.

    """
    try:
        paper_json =  read_paper_json(f_json)
        
        annot_json = {}
        annot_json['paper_id'] = paper_json['paper_id']

        for part, path in cfg.JSON_TEXT_MAP.items():
            text = get_nested_dict_value(paper_json, path[0], default='')
            lang = get_nested_dict_value(paper_json, path[1], default='fr')
            
            if text and lang:
                
                annot_json[part] = wa.request_concept_annotator(text, lang,
                                                                confidence=cfg.PYCLINREC_CONFIDENCE,
                                                                postprocess_callback=postprocess_pyclinrec_response)

        # clean out the null values, otherwise there might be problems
        #  with importing them into MongoDB
        annot_json  = {k: v for k, v in annot_json.items() if v}

        save_paper_json(f_out_json, annot_json)
        
    except Exception as e:
        logger.exception('%s: %s', f_json, str(e))

    return f_out_json


#%% 
def annotate_one(f_json):
    """
    Mapping file names and logging wrapper 

    """
    
    logger.info(f_json + '--->')
         
    filename = os.path.basename(f_json).split('.')[0] 
    
    f_out = os.path.join(cfg.OUTPUT_PATH, filename + cfg.OUTPUT_SUFFIX)  
    
    if not cfg.OUTPUT_OVERWRITE_EXISTING:
         if os.path.exists(f_out):
             logger.info(f_out + ' already exists')
             return f_out
    
    f_out = annotate_with_pyclinrec(f_json, f_out)
    logger.info(f_out)
    
    return f_out

#%%    
def annotate_documents(asynch=False):
    """
    Loop through or asynchronously process documents' json  

    """
   
    files = glob.glob(os.path.join(cfg.INPUT_PATH, cfg.INPUT_PATTERN))
    logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 
    
    if asynch:
       #files = files[:50]   # delete
       with concurrent.futures.ThreadPoolExecutor(max_workers=cfg.ASYNCH_MAX_WORKERS) as executor:
           executor.map(annotate_one, files)
           
    else:       
            
        #files = files[:5] #delete
        for f_json in files:
            annotate_one(f_json)
    
    return

#%%     
if __name__ == '__main__':
    
   # Make output directories
    os.makedirs(cfg.OUTPUT_PATH, exist_ok=True)
        
    annotate_documents(cfg.ASYNCH_PROCESSING)
    
        
close_timestamp_logger(logger)       