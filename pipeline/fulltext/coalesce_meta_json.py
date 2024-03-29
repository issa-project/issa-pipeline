# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 10:47:17 2021

@author: abobashe
"""
import os
import sys
import glob

sys.path.append('..')  
from util import read_paper_json, save_paper_json
from util import open_timestamp_logger, close_timestamp_logger
from util import merge_nested_dicts
from util import add_path_to_config  

add_path_to_config()
from config import cfg_coalesce_meta_json as cfg

#%% Set up logging
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               first_line = 'Coalesce metadata text and Grobid extracted text...')
#%% Helper functions
  
def coalesce_json(f_json, output_path):
    """
    Replace title and abstract text in Grobid extracted json files with text
    from metadata 

    Parameters:
        f_json (str): path to json file
        output_path (str): path to output directory

    Returns:
        None    
    """
    # read metadata json
    metadata_dict = read_paper_json(f_json)
    paper_id = metadata_dict['paper_id']
    logger.info(f_json + '--->')
    
    # read grobid json
    grobid_json = glob.glob(os.path.join(cfg.INPUT_FULLTEXT_PATH,  paper_id + '*.json'))
    
    coalesced_dict = {}
    if grobid_json:
        f_json = grobid_json[0]
        logger.info(f_json + '--->')
        
        coalesced_dict = read_paper_json(f_json)
        coalesced_dict = merge_nested_dicts(coalesced_dict, metadata_dict)
    else:
        coalesced_dict = metadata_dict
        logger.info('Paper %s: Grobid extraction not found, only metadata is used' % paper_id)

    # write new json
    if coalesced_dict: 
        json_path = os.path.join( cfg.OUTPUT_PATH , paper_id + cfg.OUTPUT_SUFFIX + '.json')
        save_paper_json(json_path, coalesced_dict)
        logger.info(json_path)       

    return

def coalesce_all():
    """
    Coalesce metadata text and Grobid extracted text for all json files in
    INPUT_METADATA_PATH with pattern INPUT_PATTERN

    """
    files = glob.fnmatch.filter(os.listdir(cfg.INPUT_METADATA_PATH), cfg.INPUT_PATTERN)
    logger.info('found %d files in %s with pattern %s', len(files), cfg.INPUT_METADATA_PATH, cfg.INPUT_PATTERN) 

    
    for f_json in files:
         try:
             
             f_json = os.path.join(cfg.INPUT_METADATA_PATH, f_json)
             
             coalesce_json(f_json, cfg.OUTPUT_PATH)
             
         except Exception as e:
             logger.exception(e)
    
    return

#%% Main    
if __name__ == '__main__':
    if cfg.DO_COALESE:
        coalesce_all()
    else:
        logger.info('Coalescing is turned off, to turn it on modify the DO_COALESCE flag in the config file')
        
close_timestamp_logger(logger)