# -*- coding: utf-8 -*-
"""     
Crafting directory structure for the dataset repository and saving metadata
in different formats.

Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""
import os
import sys
import pandas as pd
import shutil
import glob
import copy
import json

sys.path.append('..') 
from util import read_metadata, copy_file, set_nested_dict_value
from util import open_timestamp_logger, close_timestamp_logger, INFO, DEBUG
from util import add_path_to_config  

add_path_to_config()
from config import cfg_create_dataset_repository as cfg

#%% Set up logging
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0],
                               log_dir=cfg.LOG_PATH, 
                               file_level=DEBUG if cfg.DEBUG else INFO,
                               first_line = 'Creating dataset repository for %s/%s ...' % (cfg.DATASET_ROOT_PATH, cfg.LATEST_UPDATE) )

#%% Create dataset repository

def create_repo_structure():
    """
    Create directory structure for the dataset repository and save metadata
    in different formats. The directory structure is defined in config module 
    and should be created every time the pipeline updates the corpus metadata. 
    The structure is rooted in cfg.DATASET_ROOT_PATH and defined in cfg.FILES_LOC.
    
    """
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
        
#%% Save metadata in different formats

# Hashable collection (set) provides the fastest comparisons of file names.
# We'll be using them to check if the file already exists to avoid re-saving. 

# META_JSON_FILES is a hashable collection of all metadata json files in the dataset.
META_JSON_FILES = set([os.path.basename(f) for f in glob.glob('%s/**/*%s.json' % (cfg.DATASET_ROOT_PATH, cfg.OUTPUT_SUFFIX), recursive = True)] )

def save_metadata_json(row: pd.Series):
    """
    For each document output metadata in json format. The json schema is defined in config module.
    The json schema is a nested dictionary with keys corresponding to the metadata fields.
    The values of the keys are the values of the metadata fields.
    The json output is optional and is used to coalesce with the full text data.
    
    Parameters:
        row : pandas.Series

    Returns:
        row : pandas.Series the same as input    
    """
    filename = '%s%s.json' % (row.paper_id, cfg.OUTPUT_SUFFIX) 
    
    try: 
        # optionally output json representation of metadata                 
        if cfg.SAVE_META_JSON and (filename not in META_JSON_FILES): 
            
            json_path = os.path.join( cfg.FILES_LOC['metadata_json'] , filename)
                        
            output_dict = copy.deepcopy(cfg.JSON_SCHEMA)
            
            for (col, keys) in cfg.METADATA_TO_JSON_MAP.items():
                set_nested_dict_value(output_dict, keys, row[col])
            
            with open(json_path, 'w' , encoding='utf-8') as json_file:
                json.dump(output_dict, json_file, indent=4, ensure_ascii=False)

            logger.info('    --->%s' % json_path) 
        elif cfg.SAVE_META_JSON:
            logger.debug('    %s exists' % filename) 
                           
    except:
        logger.exception('Error in saving %s' % filename ) 
           
    return row


# META_TXT_FILES is a hashable collection of all metadata text files in the dataset.
META_TXT_FILES = set([os.path.basename(f) for f in glob.glob('%s/**/*%s.txt' % (cfg.DATASET_ROOT_PATH, cfg.OUTPUT_SUFFIX), recursive = True)] )

def save_metadata_text(row: pd.Series):
    """
    For each document output metadata in text format. 
    The text files contain title and abstract of the article.
    Output of the text files is optional  and is used to train text models.

    Parameters:
        row : pandas.Series

    Returns:
        row : pandas.Series the same as input     
    """
    filename = '%s%s.txt' % (row.paper_id, cfg.OUTPUT_SUFFIX)
    
    try: 
        if cfg.SAVE_META_TEXT  and (filename not in META_TXT_FILES) :
            
            text_path = os.path.join( cfg.FILES_LOC["txt"], filename)
            
            pd.DataFrame({'text' : [row.title , row.abstract] }) \
                         .to_csv(text_path, 
                                 sep='\t', encoding='utf-8',
                                 header=False, index=False,  
                                 line_terminator= os.linesep)
            logger.info('    --->%s' % text_path) 
        elif cfg.SAVE_META_JSON:
            logger.debug('    %s exists' % filename)                            
    except:
        logger.exception('Error in saving %s' % filename ) 
     
    return row

# PDF_URL_FILES is a hashable collection of all pdf url files in the dataset.
PDF_URL_FILES = set([os.path.basename(f) for f in glob.glob('%s/**/*.url' % (cfg.DATASET_ROOT_PATH), recursive = True)] )

def save_pdf_url(row: pd.Series):
    """
    For each document output a text file with .url extension.
    The .url files contain URLs of the PDF file found in the metadata.
    Output of the url files is optional and is used to download PDFs.

    Parameters:
        row : pandas.Series

    Returns:
        row : pandas.Series the same as input
    """
    filename = '%s.url' % row.paper_id
    pdf_url = row.pdf_url
    
    try: 
        # optionally output urls to download the pdfs   
        if cfg.SAVE_PDF_URL and pdf_url and (filename not in PDF_URL_FILES): 
                
            url_path = os.path.join(cfg.FILES_LOC["url"], filename)
    
            pd.DataFrame({'pdf_url' : [pdf_url] }) \
                        .to_csv(url_path ,
                                sep='\t', encoding='utf-8', 
                                header=False, index=False, 
                                line_terminator='\n')    
            logger.info('    --->%s' % url_path) 
        elif cfg.SAVE_META_JSON:
            logger.debug('    %s exists' % filename) 
 
    except:
        logger.exception('Error in saving %s' % filename) 
           
    return row

# TSV_LABEL_FILES is a hashable collection of all tsv label files in the dataset.
TSV_LABEL_FILES = set([os.path.basename(f) for f in glob.glob('%s/**/*.tsv' % (cfg.DATASET_ROOT_PATH), recursive = True)] )

def save_labels_tsv(row: pd.Series):
    """
    For each document save the descriptor labels in tsv format <uri> <label>. 
    Output of the tsv files is optional and is used to train text models.

    Parameters:
        row : pandas.Series

    Returns:
        row : pandas.Series the same as input
    """
    filename = '%s.tsv' %  row.paper_id
    
    try: 
        # optionally output labels for Annif
        if cfg.SAVE_LABELS_TSV and (filename not in TSV_LABEL_FILES):
                
            tsv_path = os.path.join(cfg.FILES_LOC["tsv"],  filename)
               
            uris = ['<%s>' %x for x in row.descriptor_uris]
            labels  = row.descriptor_labels
                
            pd.DataFrame({'uri' : uris, 'label' : labels}) \
                         .to_csv(tsv_path ,
                                 sep='\t',  encoding='utf-8',
                                 header=False, index=False, 
                                 line_terminator='\n')
            logger.info('    --->%s' % tsv_path) 
        elif cfg.SAVE_META_JSON:
            logger.debug('    %s exists' % filename) 

    except:
        logger.exception('Error in saving %s' % filename) 
           
    return row

#%% Helper functions
    
def _log_message(df, msg, *args):
    """
    Convenience function to log messages that can be called by the pipe.

    Parameters:
        df : pandas.DataFrame
        msg : str as in sprintf with % placeholders
        *args : list of sprintf arguments 

    Returns:
        df : pandas.DataFrame the same as input
     """

    logger.info(msg, *args)   
    return df    

def fill_missing_values(df):
    """
    Helper function to fill in the missing values in the metadata.
    -- For string columns fill in with empty string.
    -- For numeric columns fill in with 0.0.

    Parameters:
        df : pandas.DataFrame       

    Returns:
        df : pandas.DataFrame 
    """

    string_columns = df.select_dtypes(include='object').columns
    df[string_columns] = df[string_columns].fillna('')

    # Fill NaN with 0.0 for numeric columns
    numeric_columns = df.select_dtypes(include='number').columns
    df[numeric_columns] = df[numeric_columns].fillna(0.0)

    return df

#%% Processing pipeline     
def create_repository():
    """
    Create the repository structure for a dataset (initial or update). 
    Run the processing pipeline to create a dataset files from the metadata.

    Parameters:
        None

    Returns:
        None
    """
 
    # create directories to hold the dataset files
    create_repo_structure()
    
    # copy metadata
    dest_metadata_path = cfg.FILES_LOC['metadata'] 
    
    metadata_path = os.path.join(cfg.INPUT_PATH, cfg.RAW_METADATA_FILENAME)    
    copy_file(metadata_path , dest_metadata_path)
    
    metadata_path = os.path.join(cfg.INPUT_PATH, cfg.INPUT_METADATA_FILENAME)
    copy_file(metadata_path , dest_metadata_path)
    
    # create files from metadata
    (read_metadata(metadata_path)
         .pipe(lambda _df: _df.astype({'paper_id': str}))
         #.pipe(lambda _df: _df.loc[_df.type == 'article'])
         #.pipe(lambda _df: _df.loc[_df.license_access == 'info:eu-repo/semantics/openAccess'])
         #.pipe(lambda _df: _df.fillna({'title':'', 'abstract':''}))
         .pipe(lambda _df: fill_missing_values(_df) )
         .pipe(_log_message, '...Output %s/%s set  ...' , cfg.DATASET_NAME, cfg.CURRENT_DATE )
         .pipe(_log_message, '   saving metadata json   ...' )
         .pipe(lambda _df: _df.apply(save_metadata_json, axis=1) )
         #.pipe(_log_message, ' for articles only:' )
         #.pipe(lambda _df: _df.loc[_df.type == 'article'])
         .pipe(_log_message, '   saving pdf urls  ...' )
         .pipe(lambda _df: _df.apply(save_pdf_url, axis=1))
         .pipe(_log_message, '   saving metadata text   ...' )
         .pipe(lambda _df: _df.apply(save_metadata_text, axis=1) )
         .pipe(_log_message, '   saving descriptor label files  ...' )
         .pipe(lambda _df: _df.apply(save_labels_tsv, axis=1))
         )


#%%  Main processing loop 
# This is the main processing loop that is called from the command line

if __name__ == '__main__':
    create_repository()

close_timestamp_logger(logger)



