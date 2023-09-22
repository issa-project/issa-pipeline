# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 10:45:04 2022

@author: abobashe
"""

import os
import sys
import glob
import shutil

from sklearn.model_selection import train_test_split

sys.path.append('..')  
from util import open_timestamp_logger, close_timestamp_logger
from util import get_nested_dict_value
from util import read_paper_json, read_metadata
from util import add_path_to_config

add_path_to_config()
from config import cfg_indexing_training as cfg

#%%
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               first_line = 'Creating training and testing data for Annif training...')
#%%
def create_training_dirs():
    """
    Make directories for training data according to the config

    """
    
    for lang, dirs in cfg.TRAINING_FILES_LOC.items():
        for _ , path in dirs.items(): 
            os.makedirs(path, exist_ok=True)

#%%
def get_language(json_dict):
    """
    Determine the language of the document because each language has its own models'

    """
    lang=''
    for part in cfg.LANGUAGE_DETERMINATORS:
        lang = get_nested_dict_value(json_dict, cfg.JSON_TEXT_MAP[part][1], default='unk' )
        if lang in cfg.TRAINING_FILES_LOC.keys():
            return lang
    
    if not lang:
        raise UserWarning('Cannot determine the language')
        
    if lang not in cfg.TRAINING_FILES_LOC.keys():
        raise UserWarning('text in  %s cannot be indexed' % lang )
    
#%%
def preprocess_one(f_json, f_txt):
    """
    Copy relevant text fields from json file into text file

    """
    try:
        paper_json = read_paper_json(f_json)
        
        lang= get_language(paper_json)
        
        text = cfg.PARTS_SEPARATOR.join( [ get_nested_dict_value(paper_json, v[0]) 
                                           for k,v in cfg.JSON_TEXT_MAP.items() 
                                           if get_nested_dict_value(paper_json, v[1]) == lang] ) 
        text = text.strip()
        
        #change the file extension to indicate the language
        f_txt = f_txt.replace('lang', lang )

        if len(text) < cfg.MIN_TEXT_LENGTH: 
           raise UserWarning('text is too short for training:', text )        
        
        with open(f_txt, 'w',  encoding='utf-8') as txt_file:
                txt_file.write(text)
        
    except UserWarning as e:
        logger.info(e)
        return ''
    
    except Exception as e:
        logger.exception(e)

    return f_txt       

def preprocess_json_to_text():
    """
    Loop through the json files to create text files

    """    
   
    files = glob.glob(os.path.join(cfg.INPUT_PATH, cfg.INPUT_PATTERN), recursive=True)
    logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 

     
    for f_json in files:
         #f_json = os.path.join(json_path, f_json)
         logger.info(f_json + '--->')
         
         filename = os.path.basename(f_json).split('.')[0]
         f_txt = os.path.join(cfg.OUTPUT_PATH, 'lang',  filename + cfg.OUTPUT_SUFFIX)  

         f_txt = preprocess_one(f_json, f_txt)
         logger.info(f_txt)
    
    return

#%%
def split_files():
    """
    Split dataset for each language into train and test sets

    """
   
    for lang in cfg.TRAINING_FILES_LOC.keys():
        
        files = glob.glob(os.path.join(cfg.OUTPUT_PATH, lang, '*.txt'))    
       
        train_files, test_files = train_test_split(files, test_size=0.2, random_state=42)
        
        logger.info('split %d files into %d train and %d test sets', len(files), len(train_files), len(test_files)) 
       
        for f_txt in train_files:
            logger.info(f_txt + '--->')
            f_dest = f_txt.replace(lang, '%s/train' % lang)
            shutil.move(f_txt, f_dest)
            logger.info(f_dest)
    
        for f_txt in test_files:
            logger.info(f_txt + '--->')
            f_dest = f_txt.replace(lang, '%s/test' % lang)
            shutil.move(f_txt, f_dest)
            logger.info(f_dest)              
      
    return 
  
#%%
def copy_label_files():
    """
    Copy corresponding label files to the test and train sets

    """
    
    files = glob.glob(os.path.join(cfg.OUTPUT_PATH, '**/*.txt'), recursive=True)
    logger.info('copy %d labels files', len(files) ) 
    
       
    for f_txt in files:
        filename = os.path.basename(f_txt).split('.')[0] + '.tsv'
        dest_dir = os.path.dirname(f_txt)
        
        files = glob.glob(os.path.join(cfg.DATASET_ROOT_PATH, cfg.LABEL_PATTERN, filename ),
                          recursive = True)
            
        if files:
            f_tsv = files[0]
        else:
            logger.error('cannot find file %s.tsv in the dataset %s', filename, cfg.DATASET_ROOT_PATH)
            continue
    
        logger.info(f_tsv + '--->')
    
        f_dest = shutil.copy(f_tsv, dest_dir)
        logger.info(f_dest)
      
    return    

import pandas as pd
def generate_label_files():
    """
    Create label files from metadata

    """
    
    files = glob.glob(os.path.join(cfg.OUTPUT_PATH, '**/*.txt'), recursive=True)
    logger.info('create %d labels files', len(files) ) 
    
    metadata = read_metadata(cfg.METADATA_FILE)
    metadata.set_index('paper_id', inplace=True)
       
    for f_txt in files:
        dest_dir = os.path.dirname(f_txt)
        paper_id = os.path.basename(f_txt).split('.')[0]      
        f_tsv = os.path.join(dest_dir, paper_id + '.tsv')
      
        try:
            row = metadata[paper_id]
        
            uris = ['<%s>' %x for x in row.descriptors_uris]
            labels  = row.descriptors_labels
    
            pd.DataFrame({'uri' : uris, 'label' : labels}) \
                         .to_csv(f_tsv ,
                                 sep='\t',  encoding='utf-8',
                                 header=False, index=False, 
                                 line_terminator='\n')
            logger.info('    --->%s' % f_tsv) 

        except:
            logger.exception('Error in saving %s' % f_tsv) 
            continue
      
    return    

#%%     
if __name__ == '__main__':
    create_training_dirs()
    
    preprocess_json_to_text()
    
    split_files()
    
    copy_label_files()
        
close_timestamp_logger(logger)

#TODO: cross-validation datasets