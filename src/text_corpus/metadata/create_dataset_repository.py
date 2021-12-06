# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""

import pandas as pd

import os
import sys
import shutil

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
    
    root_path = os.path.realpath(os.path.normpath(cfg.OUTPUT_ROOT_PATH))
    if not os.path.exists(root_path):
        #os.makedirs(cfg.OUTPUT_ROOT_PATH)
        os.makedirs(root_path)

    dataset_path = os.path.join(cfg.OUTPUT_ROOT_PATH, cfg.DATASET_NAME)
    dataset_path = os.path.realpath(os.path.normpath(dataset_path))
        
    if os.path.exists(dataset_path) and cfg.REMOVE_FILES:
        shutil.rmtree(dataset_path, ignore_errors=True)    
       
    for ext, path in cfg.FILES_LOC.items():
        path = os.path.realpath(os.path.normpath(path))
        os.makedirs(path, exist_ok=True)

    logger.info('dataset repository: %s/%s' , dataset_path, cfg.LANGUAGE)
        
    return dataset_path
        

#%%

def create_dataset_files(row):
    
    filename = row.agritrop_id
    
    try: 
        # optionally output labels for Annif
        if cfg.SAVE_LABELS_TSV:
            tsv_path = os.path.join(cfg.FILES_LOC["tsv"], filename + '.tsv')
            tsv_path = os.path.realpath(os.path.normpath(tsv_path))
               
            uris = ['<%s>' %x for x in row.agrovoc_uris]
            labels  = row.agrovoc_labels
    
            pd.DataFrame({'uri' : uris, 'label' : labels}) \
                         .to_csv(tsv_path ,
                                 sep='\t',  encoding='utf-8',
                                 header=False, index=False, 
                                 line_terminator='\n')
         
        
        # optionally output urls to download the pdfs   
        if cfg.SAVE_PDF_URL:    
            url_path = os.path.join(cfg.FILES_LOC["url"], filename + '.url')
            url_path = os.path.realpath(os.path.normpath(url_path))
    
            pd.DataFrame({'pdf_url' : [row.pdf_url] }) \
                        .to_csv(url_path ,
                                sep='\t', encoding='utf-8', 
                                header=False, index=False, 
                                line_terminator='\n')
        
        # optionally output available text to a text file 
        if cfg.SAVE_TITLE_ABSTRACT_TEXT:
            text_path = os.path.join( cfg.FILES_LOC["txt"], filename + cfg.OUTPUT_SUFFIX + '.txt')
            text_path = os.path.realpath(os.path.normpath(text_path))
            
            pd.DataFrame({'text' : [row.title , row.abstract] }) \
                         .to_csv(text_path, 
                                 sep='\t', encoding='utf-8',
                                 header=False, index=False,  
                                 line_terminator='\n')
                         
        # optionally output json representation of metadata                 
        if cfg.SAVE_TITLE_ABSTRACT_JSON:
            json_path = os.path.join( cfg.FILES_LOC['metadata_json'] , filename + cfg.JSON_SUFFIX + '.json')
            json_path = os.path.realpath(os.path.normpath(json_path))
            
            output_dict = cfg.JSON_SCHEMA.copy()
            
            for (col, keys) in cfg.DATAFRAME_TO_JSON_MAP.items():
                set_nested_dict_value(output_dict, keys, row[col])
            
            with open(json_path, 'w' , encoding='utf-8') as json_file:
                json.dump(output_dict, json_file, indent=4, ensure_ascii=False)
                           
    except:
           logger.exception("Errpr in processing document %s" % filename) 
           
    return filename

def id_to_string(df):
    
    df.agritrop_id = df.agritrop_id.astype(str)
    
    #df = df.astype({'argitrop_id': str})
    
    return df
    
def create_dataset(df):
    try:
       
        logger.info('...Output %s set  ...' , cfg.DATASET_NAME)   
        df.fillna('').apply(lambda row: create_dataset_files(row), axis=1)
            
    except:        
        logger.exception('Error in % set output:', cfg.DATASET_NAME)
        
    return df    

#%%     
def main():
    
    # create directories to hold the dataset files
    create_repo_structure()
    
    #copy metadata
    meatadata_path = os.path.join(cfg.INPUT_PATH, cfg.PROCESSED_DATA_FILENAME)
    dest_metadata_path = cfg.FILES_LOC['metadata'] #os.path.join(create_repo_structure(), cfg.LANGUAGE)
    
    copy_file(meatadata_path , dest_metadata_path)
    
    # create files from metadata
    
    (read_metadata(meatadata_path)
         .pipe(id_to_string)
         .pipe(create_dataset))

    # return the repository structure in case that the caller wants to use it
    return cfg.FILES_LOC

#%%

if __name__ == '__main__':
    main()

close_timestamp_logger(logger)



