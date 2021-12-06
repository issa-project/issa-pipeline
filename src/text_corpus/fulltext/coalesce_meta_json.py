# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 10:47:17 2021

@author: abobashe
"""
import os
import sys
import glob

sys.path.append('..')  

from config import cfg_coalesce_meta_json as cfg
from util import read_metadata
from util import read_paper_json, save_paper_json
from util import open_timestamp_logger, close_timestamp_logger
from util import set_nested_dict_value

#%% 
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               first_line = 'Coalesce metadata text and Grobid exrtacted text...')
#%%
def coalesce_one(row):
    """
    Replace title and abstract text in grobid extracted json files with metadata
    
    Parameters
    ----------
    row : pandas.DataRow
        Row in the pandas Dataframe representing the paper's metadata.

    Returns
    -------
    None.

    """
    
    metadata_dict = cfg.JSON_SCHEMA.copy()
            
    for (col, keys) in cfg.DATAFRAME_TO_JSON_MAP.items():
        set_nested_dict_value(metadata_dict, keys, row[col])
    
    #make sure that the paper id is a string
    if not isinstance(metadata_dict['paper_id'], str) : 
        metadata_dict['paper_id'] = str(metadata_dict['paper_id'])
        
    paper_id = metadata_dict['paper_id']
    
    #read grobid json
    grobid_json = glob.glob(os.path.join(cfg.GROBID_JSON_PATH,  paper_id + '*.*'))
    
    coalesced_dict = {}
    if grobid_json:
        coalesced_dict = read_paper_json(grobid_json[0])
        # merge two dictionaries, the values from the second dictionary 
        # replace matched properties values
        coalesced_dict = { **coalesced_dict, **metadata_dict }
        logger.info('Paper %s: Replaced title and abstract with metadata' % paper_id)
    else:
        coalesced_dict = metadata_dict
        logger.info('Paper %s: Grobid extraction not found, only metadata is saved' % paper_id)

    if coalesced_dict: 
        json_path = os.path.join( cfg.FILES_LOC['coalesced_json'] , paper_id + cfg.JSON_SUFFIX + '.json')
        save_paper_json(json_path, coalesced_dict)
                

def coalesce_all():
    
    (read_metadata(cfg.METADATA_FILE)
     .pipe(lambda df_: df_.apply(coalesce_one, axis=1)))



#%%     
if __name__ == '__main__':
    if cfg.DO_COALESE:
        coalesce_all()
    else:
        logger.info('Coalescing is turned off, to turn it on modify the DO_COALESCE flag in the config file')
        
close_timestamp_logger(logger)