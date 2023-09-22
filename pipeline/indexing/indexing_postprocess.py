# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 19:11:36 2022

@author: abobashe
"""

import os
import sys
import glob

import pandas as pd

sys.path.append('..')  
from util import save_paper_json
from util import open_timestamp_logger, close_timestamp_logger
from util import add_path_to_config  

add_path_to_config()
from config import cfg_indexing_postprocess as cfg

#%% 
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               first_line = 'Postprocessing subjects tsv files for Annif indexing...')
#%%
def postprocess_one(f_tsv, f_json):
    """
    Reformat output of Annif indexing (tsv file) into json 

    """
    try:
        paper_id = os.path.basename(f_tsv).split('.')[0]
        model = os.path.basename(f_tsv).split('.')[1]
        lang  = os.path.basename(os.path.dirname(f_tsv) )
        
        json_dict = cfg.OUTPUT_SCHEMA.copy()
        json_dict['paper_id'] = paper_id
        json_dict['model'] = model
        json_dict['language'] = lang

        columns = list(cfg.OUTPUT_SCHEMA['subjects'][0].keys())
        subjects_df = pd.read_csv(f_tsv, sep='\t', encoding='utf-8', header=None, names=columns[:-1])
        subjects_df['rank'] = subjects_df.index + 1
        subjects_df.columns = columns
        subjects_df['uri'] = subjects_df['uri'].str.strip('<>')
      
        json_dict['subjects'] = subjects_df.to_dict(orient='records')
        
        save_paper_json(f_json, json_dict)
    
    except Exception as e:
        logger.exception(e)

    return f_json
        
#%%
def postprocess_tsv_to_json():
    """
    Loop over output files produced by Annif indexing

    """
    files = glob.glob(os.path.join(cfg.INPUT_TSV_PATH, cfg.INPUT_PATTERN), recursive=True )
    logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 
    
    for f_tsv in files:
        logger.info(f_tsv + '--->')
        
        filename = os.path.basename(f_tsv).split('.')[0]
        
        f_json = os.path.join(cfg.OUTPUT_JSON_PATH, filename + cfg.OUTPUT_SUFFIX)
    
        postprocess_one(f_tsv, f_json)
        
        logger.info(f_json)
       
    return

#%%     
if __name__ == '__main__':
    postprocess_tsv_to_json()
        
close_timestamp_logger(logger)