# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 10:45:04 2022

@author: abobashe
"""

import os
import sys
import glob
import shutil
import pandas as pd

from sklearn.model_selection import train_test_split

print(os.getcwd())

sys.path.append('..')  
from util import open_timestamp_logger, close_timestamp_logger
from util import get_nested_dict_value
from util import read_paper_json, read_metadata
from util import add_path_to_config

add_path_to_config()
from config import cfg_indexing_training as cfg

#%% Set up logging
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               first_line = 'Creating training and testing data for Annif training...')
#%% Language determination 
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
        lang = get_nested_dict_value(json_dict,  cfg.JSON_TEXT_MAP[part][1] + ['code'], default='' )
        score = get_nested_dict_value(json_dict, cfg.JSON_TEXT_MAP[part][1] + ['score'], default=0.0 )
        if lang in cfg.TRAINING_FILES_LOC.keys() and score > cfg.LANGUAGE_SCORE_THRESHOLD:
            return lang
    
    if not lang:
        raise UserWarning('cannot determine the language')
        
    if lang not in cfg.TRAINING_FILES_LOC.keys():
        raise UserWarning('text in  %s cannot be indexed' % lang )

    if score < cfg.LANGUAGE_SCORE_THRESHOLD:
        raise UserWarning('language score is too low %f' % score )
    
#%% Helper functions to create text data
def create_training_dirs():
    """
    Make directories for training data according to the config

    """
    for lang, dirs in cfg.TRAINING_FILES_LOC.items():
        for _ , path in dirs.items(): 
            os.makedirs(path, exist_ok=True)
            

def preprocess_one(f_json, f_txt):
    """
    Copy relevant text fields from json file into text file

    Parameters:
        f_json (str): path to json file
        f_txt (str): path to output text file

    Returns:
        f_txt (str): path to output text file
    """
    try:
        paper_json = read_paper_json(f_json)

        title = get_nested_dict_value(paper_json, cfg.JSON_TEXT_MAP['title'][0], default='')
        abstract = get_nested_dict_value(paper_json, cfg.JSON_TEXT_MAP['abstract'][0], default='')
        body = get_nested_dict_value(paper_json, cfg.JSON_TEXT_MAP['body_text'][0], default='')

        if not abstract and not body:
            raise UserWarning('no abstract or body text in the document')

        lang= get_language(paper_json)
        
        text = cfg.PARTS_SEPARATOR.join( [ get_nested_dict_value(paper_json, v[0], default='') 
                                           for k,v in cfg.JSON_TEXT_MAP.items() 
                                           if get_nested_dict_value(paper_json, v[1] + ['code'], default='unk') == lang] ) 
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
    Loop through the documents' json files to create text files

    """    
    files = glob.glob(os.path.join(cfg.INPUT_PATH, cfg.INPUT_PATTERN), recursive=True)
    logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 

    # Sort files by the number in the file name and take the first FILES_SET_SIZE files
    files = sorted(files, key=cfg.FILES_SORT_KEY )
    files = files[:cfg.FILES_SET_SIZE] 
    logger.info('taking %d files; last paper ID is %s', len(files), os.path.basename(files[-1]).split('.')[0])
     
    for f_json in files:
         logger.info(f_json + '--->')
         
         filename = os.path.basename(f_json).split('.')[0]
         f_txt = os.path.join(cfg.OUTPUT_PATH, 'lang',  filename + cfg.OUTPUT_SUFFIX)  

         f_txt = preprocess_one(f_json, f_txt)
         logger.info(f_txt)
    
    return


  
#%% Helper function to create labels
def copy_label_files():
    """
    Copy corresponding label files to the test and train sets.
    Note that the label files have to be created while running 
    the /pipeline/metadata/create_data_repository.py script with
    cfg.SAVE_LABELS_TSV=True   

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

def generate_label_files():
    """
    Create label files from metadata. This function is used when the label files
    were not created while running the /pipeline/metadata/create_data_repository.py
   
   """
    files = glob.glob(os.path.join(cfg.OUTPUT_PATH, '**/*.txt'), recursive=True)
    logger.info('create %d label files', len(files) ) 

    metadata_file = os.path.join(cfg.INPUT_PATH,
                                 sorted(os.listdir(cfg.INPUT_PATH), reverse=True) [0], #LATEST_UPDATE,
                                 cfg.METADATA_FILENAME)
    
    metadata = read_metadata(metadata_file)
    metadata['paper_id'] = metadata['paper_id'].astype(str)
    metadata.set_index('paper_id', inplace=True)
       
    for f_txt in files:
        dest_dir = os.path.dirname(f_txt)
        paper_id = os.path.basename(f_txt).split('.')[0]      
        f_tsv = os.path.join(dest_dir, paper_id + '.tsv')
      
        try:
            row = metadata.loc[paper_id]

            uris = ['<%s>' %x for x in row.descriptor_uris]
            labels  = row.descriptor_labels
    
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

def remove_not_labeled_files():
    """
    Remove empty label files and associated text file from the dataset

    """
    files = glob.glob(os.path.join(cfg.OUTPUT_PATH, '**/*.tsv'), recursive=True)
    logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 

    for f_tsv in files:
        if os.stat(f_tsv).st_size == 0:
            f_txt = os.path.splitext(f_tsv)[0] + '.txt'
            logger.info('removing not labeled text %s', f_txt)
            os.remove(f_tsv)
            os.remove(f_txt)
        
    return

 #%% Create train and test sets
def split_train_test_files():
    """
    Split dataset for each language into train and test sets

    """
    for lang in cfg.TRAINING_FILES_LOC.keys():
        
        files = glob.glob(os.path.join(cfg.OUTPUT_PATH, lang, '*.txt'))    
       
        train_files, test_files = train_test_split(files, test_size=cfg.TEST_SET_SPLIT, random_state=42)
        
        logger.info('split %d files into %d train and %d test sets', len(files), len(train_files), len(test_files)) 
       
        for sub_dir, file_list in {'train' : train_files, 'test': test_files}.items():
            dest_dir = cfg.TRAINING_FILES_LOC[lang][sub_dir] 
            shutil.rmtree(dest_dir, ignore_errors=True)
            os.makedirs(dest_dir, exist_ok=True)
   
            for f_txt in file_list:
                f_tsv = os.path.splitext(f_txt)[0] + '.tsv'
                logger.info(f_txt + '--->')
                logger.info(f_tsv + '--->')
                shutil.move(f_txt, dest_dir)
                shutil.move(f_tsv, dest_dir)
                logger.info(dest_dir)
      
    return       

def count_files():
    """
    Count files in each directory

    """
    for lang in cfg.TRAINING_FILES_LOC.keys():
        for sub_dir in ['train', 'test']:
            dest_dir = cfg.TRAINING_FILES_LOC[lang][sub_dir] 
            files = glob.glob(os.path.join(dest_dir, '**/*.txt'), recursive=True)
            logger.info('%d files in %s', len(files), dest_dir) 
      
    return
#%% Main 
if __name__ == '__main__':
    create_training_dirs()
    
    preprocess_json_to_text()
    
    if cfg.CREATE_LABELS:
        generate_label_files()
    else:
        copy_label_files()

    remove_not_labeled_files()

    split_train_test_files()

    count_files()
        
close_timestamp_logger(logger)

#TODO: cross-validation datasets