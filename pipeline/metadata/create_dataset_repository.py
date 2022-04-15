# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""

import pandas as pd

import os
import sys
import shutil
import glob

import json

sys.path.append('..')

from util import read_metadata, copy_file, set_nested_dict_value
from config import cfg_create_dataset_repository as cfg

#%%
from util import open_timestamp_logger, close_timestamp_logger

logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0],
                               log_dir=cfg.LOG_PATH, 
                               first_line = 'Creating dataset repository...')

#%%
def create_repo_structure():
    """
    Create the directory structure for the data itteration

    """
    
#    root_path = os.path.realpath(os.path.normpath(cfg.OUTPUT_ROOT_PATH))
#    if not os.path.exists(root_path):
#        os.makedirs(root_path)

    #dataset_path = os.path.join(cfg.OUTPUT_ROOT_PATH, cfg.DATASET_NAME)
    dataset_path = os.path.realpath(cfg.DATASET_ROOT_PATH)
        
    if os.path.exists(dataset_path) and cfg.REMOVE_FILES:
        shutil.rmtree(dataset_path, ignore_errors=True)  
     
    for key, path in cfg.FILES_LOC.items():
        path= path.replace(cfg.LATEST_UPDATE , cfg.CURRENT_DATE)
        #path = os.path.realpath(os.path.normpath(path))
        os.makedirs(path, exist_ok=True)
        cfg.FILES_LOC[key] = path

    logger.info('dataset repository: %s/%s' , dataset_path, cfg.CURRENT_DATE)
        
    return dataset_path
        

#%%
def save_metadata_json(row):
    """
    For each article create metadata json representtaion 

    """
    
    filename = '%s%s.json' % (row.agritrop_id, cfg.OUTPUT_SUFFIX) 
    
    try: 
        # optionally output json representation of metadata                 
        if cfg.SAVE_META_JSON and \
            not glob.glob('%s/**/%s' % (cfg.DATASET_ROOT_PATH, filename),
                          recursive = True):
            
            json_path = os.path.join( cfg.FILES_LOC['metadata_json'] , filename)
                        
            output_dict = cfg.JSON_SCHEMA.copy()
            
            for (col, keys) in cfg.METADATA_TO_JSON_MAP.items():
                set_nested_dict_value(output_dict, keys, row[col])
            
            with open(json_path, 'w' , encoding='utf-8') as json_file:
                json.dump(output_dict, json_file, indent=4, ensure_ascii=False)
                           
    except:
           logger.exception('Error in saving %s' % filename ) 
           
    return row

def save_metadata_text(row):
    """
    For each article output only text fields. Can be used in text model training.

    """
    
    filename = '%s%s.txt' % (row.agritrop_id, cfg.OUTPUT_SUFFIX)
    
    try: 
        # optionally output available text to a text file 
        if cfg.SAVE_META_TEXT  and \
            not glob.glob('%s/**/%s' % (cfg.DATASET_ROOT_PATH, filename), recursive = True):
            
            text_path = os.path.join( cfg.FILES_LOC["txt"], filename)
            #text_path = os.path.realpath(os.path.normpath(text_path))
            
            pd.DataFrame({'text' : [row.title , row.abstract] }) \
                         .to_csv(text_path, 
                                 sep='\t', encoding='utf-8',
                                 header=False, index=False,  
                                 line_terminator= os.linesep)
                           
    except:
           logger.exception('Error in saving %s' % filename ) 
     
    return row

def save_pdf_url(row):
    """
    For each article save file with a url of the pdf

    """
    
    filename = '%s.url' % row.agritrop_id
    
    try: 
        # optionally output urls to download the pdfs   
        if cfg.SAVE_PDF_URL and \
            not glob.glob('%s/**/%s' % (cfg.DATASET_ROOT_PATH, filename),
                          recursive = True):
                
            url_path = os.path.join(cfg.FILES_LOC["url"], filename)
            #url_path = os.path.realpath(os.path.normpath(url_path))
    
            pd.DataFrame({'pdf_url' : [row.pdf_url] }) \
                        .to_csv(url_path ,
                                sep='\t', encoding='utf-8', 
                                header=False, index=False, 
                                line_terminator='\n')
        
    except:
           logger.exception('Error in saving %s' % filename) 
           
    return row


def save_agrovoc_lables(row):
    """
    For each artile ave the agrovoc lables. Can be used in model training

    """
    
    filename = '%s.tsv' %  row.agritrop_id
    
    try: 
        # optionally output labels for Annif
        if cfg.SAVE_LABELS_TSV and \
            not glob.glob('%s/**/%s' % (cfg.DATASET_ROOT_PATH, filename),
                          recursive = True):
                
            tsv_path = os.path.join(cfg.FILES_LOC["tsv"],  filename)
            #tsv_path = os.path.realpath(os.path.normpath(tsv_path))
               
            uris = ['<%s>' %x for x in row.agrovoc_uris]
            labels  = row.agrovoc_labels
    
            pd.DataFrame({'uri' : uris, 'label' : labels}) \
                         .to_csv(tsv_path ,
                                 sep='\t',  encoding='utf-8',
                                 header=False, index=False, 
                                 line_terminator='\n')
    except:
           logger.exception('Error in saving %s' % filename) 
           
    return row
    
def _log_message(df, msg, *args):
    logger.info(msg, *args)   
    return df    


#%%     
def create_dataset():
    
    # create directories to hold the dataset files
    create_repo_structure()
    
    # copy metadata
    metadata_path = os.path.join(cfg.INPUT_PATH, cfg.INPUT_METADATA_FILENAME)
    dest_metadata_path = cfg.FILES_LOC['metadata'] #os.path.join(create_repo_structure(), cfg.LANGUAGE)
    
    copy_file(metadata_path , dest_metadata_path)
    
    # create files from metadata
    (read_metadata(metadata_path)
         .pipe(lambda _df: _df.astype({'agritrop_id': str}))
         .pipe(lambda _df: _df.loc[_df.type == 'article'])
         .pipe(lambda _df: _df.fillna({'title':'', 'abstract':''}))
         .pipe(_log_message, '...Output %s/%s set  ...' , cfg.DATASET_NAME, cfg.CURRENT_DATE )
         .pipe(lambda _df: _df.apply(save_metadata_json, axis=1) )
         .pipe(lambda _df: _df.apply(save_metadata_text, axis=1) )
         .pipe(lambda _df: _df.apply(save_pdf_url, axis=1))
         .pipe(lambda _df: _df.apply(save_agrovoc_lables, axis=1))
         )

    # return the repository structure in case that the caller wants to use it
    return cfg.FILES_LOC

#%%

if __name__ == '__main__':
    create_dataset()

close_timestamp_logger(logger)



