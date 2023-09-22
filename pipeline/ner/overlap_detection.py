# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 13:52:49 2022

@author: abobashe
"""

import os
import sys
import glob
import concurrent.futures

import json
#from  jsonpath_ng import parse

#import pandas as pd
#from  numpy import nan
#import datetime

sys.path.append('..')  
from util import read_paper_json, save_paper_json
from util import open_timestamp_logger, close_timestamp_logger
from util import get_nested_dict_value, set_nested_dict_value
from util import add_path_to_config

add_path_to_config()
from config import cfg_overlap_detection as cfg

#%% 
from logging import INFO, DEBUG


logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               file_level=DEBUG if cfg.DEBUG else INFO,
                               first_line = 'Detecting overlapping named entities ...')
#%%
# 
def _strlen(v):
    """
    Helper function to convert possible non-string values to a string and measure the length
    """
    return len(str(v))

#%%
def is_overlap(terms , text_elem_name='surfaceForm', offset_elem_name='offset' ):
    """
    Determines if the given terms overlap in the string based on their offsets.

    Args:
    - terms (list): A list of tuples, each containing the term and its offset in the string.

    Returns:
    - bool: True if the terms overlap, False otherwise.
    """
    # Sort the terms based on their starting offset
    terms = sorted(terms, key=lambda x: x[offset_elem_name])

    # Check if the end offset of the previous term is greater than the start offset of the current term
    for i in range(1, len(terms)):
        if terms[i][offset_elem_name] < terms[i-1][offset_elem_name] + _strlen(terms[i-1][text_elem_name]):
            return True

    return False

def remove_overlaps(terms, text_elem_name='surfaceForm', 
                                            offset_elem_name='offset', 
                                            score_elem_name='similarityScore',
                                            how='length'):
    """
    Removes the annotations with the lowest confidence score in the overlapping terms passed as a list.

    """
    # Sort the terms based on their starting offset
    terms = sorted(terms, key=lambda x: x[offset_elem_name])

    # Check if the end offset of the previous term is greater than the start offset of the current term
    remove_idx = []
    for i in range(1, len(terms)):
        j = i-1
        # check if a previous term is already marked
        while ('overlap' in terms[j].keys() ): 
            j -= 1

        if terms[i][offset_elem_name] < terms[j][offset_elem_name] + _strlen(terms[j][text_elem_name]):

            if how == 'length':
                remove_idx.append( j if _strlen(terms[j][text_elem_name]) < _strlen(terms[i][text_elem_name]) else i) 

            elif how == 'score':
                remove_idx.append( j if terms[j][score_elem_name] < terms[i][score_elem_name]  else i) 

    remove_idx = sorted(remove_idx, reverse=True)

    for i in remove_idx:
        terms.pop(i)

    return terms

def mark_overlaps(terms, text_elem_name='surfaceForm', 
                         offset_elem_name='offset', 
                         score_elem_name='similarityScore',
                         how='length'): # or 'score'):
    """
    Removes the annotations with the lowest confidence score in the overlapping terms passed as a list.

    """

    # Sort the terms based on their starting offset
    terms = sorted(terms, key=lambda x: x[offset_elem_name])

    # Clear previous flags to allow multiple reprocessing
    _ = [t.pop('overlap', '') for t in terms]

    # Check if the end offset of the previous term is greater than the start offset of the current term
    remove_idx = []
    for i in range(1, len(terms)):
        j = i-1
        # check if a previous term is already marked
        while ('overlap' in terms[j].keys() ): 
            j -= 1

        if terms[i][offset_elem_name] < terms[j][offset_elem_name] + _strlen(terms[j][text_elem_name]):
            
            if how == 'length':
                idx = j if _strlen(terms[j][text_elem_name]) < _strlen(terms[i][text_elem_name]) else i

            else:
                idx = j if terms[j][score_elem_name] < terms[i][score_elem_name]  else i

            terms[idx]['overlap'] = True

            logger.debug('    overlap detected: "%s" (%d) and "%s" (%d)', terms[j][text_elem_name], terms[j][offset_elem_name],
                                                                          terms[i][text_elem_name], terms[i][offset_elem_name]   )

    return terms

#%%
def detect_overlaps(f_json, f_out_json):
    """
    
    """
    try:
        annot_json =  read_paper_json(f_json)

        annot_hash = hash(json.dumps(annot_json, sort_keys=True).encode('utf-8') )
        
        for path_to_terms, text_el, offset_el, score_el, how in cfg.JSON_MAP.values():
            try:
                if cfg.REMOVE_OVERLAPS:
                    new_json= remove_overlaps(get_nested_dict_value(annot_json, path_to_terms),
                                    text_el, offset_el, score_el, 
                                    how )
                else:
                    new_json= mark_overlaps(get_nested_dict_value(annot_json, path_to_terms),
                                    text_el, offset_el, score_el, 
                                    how )
                set_nested_dict_value(annot_json, path_to_terms, new_json)

            except KeyError as e:
                logger.debug('    KeyError: %s', e.args[0]) 
                pass

        # verify if changes were made
        if annot_hash !=  hash(json.dumps(annot_json, sort_keys=True).encode('utf-8') ):
            save_paper_json(f_out_json, annot_json)
        
    except Exception as e:
        logger.exception('%s: %s', f_json, str(e))

    return f_out_json


#%% 
def detect_overlaps_file(f_json):
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
    
    f_out = detect_overlaps(f_json, f_out)
    logger.info(f_out)
    
    return f_out

#%%    
def detect_overlaps_dir():
    """
    Loop through or asynchronously process the NER output files 

    """
  
    files = glob.glob(os.path.join(cfg.INPUT_PATH, cfg.INPUT_PATTERN))
    logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 

    if cfg.ASYNCH_PROCESSING:
       with concurrent.futures.ThreadPoolExecutor(max_workers=cfg.ASYNCH_MAX_WORKERS) as executor:
           executor.map(detect_overlaps_file, files)
           
    else:       
        for f_json in files:
            detect_overlaps_file(f_json)
            
    
    return

#%%     
if __name__ == '__main__':
        
    for config in cfg.CONFIG_MAP:
        cfg.INPUT_PATH, cfg.OUTPUT_PATH, cfg.JSON_MAP = cfg.CONFIG_MAP[config].values()

        os.makedirs(cfg.OUTPUT_PATH, exist_ok=True)
        detect_overlaps_dir()
        
close_timestamp_logger(logger)       
