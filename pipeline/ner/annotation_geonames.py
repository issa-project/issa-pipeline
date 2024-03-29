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

import pandas as pd
from  numpy import nan
import datetime

sys.path.append('..')  
from util import read_paper_json, save_paper_json
from util import open_timestamp_logger, close_timestamp_logger
from util import get_nested_dict_value
from util import add_path_to_config

add_path_to_config()
from config import cfg_annotation_geonames as cfg

from wrapper_annotator import WrapperAnnotator
wa = WrapperAnnotator(entity_fishing_endpoint= cfg.ENTITY_FISHING_ENDPOINTS ,
                      timeout=cfg.REQUEST_TIMEOUT )

#%% 
from logging import INFO, DEBUG
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               file_level=DEBUG if cfg.DEBUG else INFO,
                               first_line = 'Annotating text with GeoNames NER service...')
#%%
def disambiguate_location(rawName, lang='en'):
    """
    If an NE is returned without WikidataID but with type LOCATION
    try to disambiguate it by sending its text as a "short" text to 
    entity-fishing disambiguation service.

    """
    
    response_json = wa.request_entity_fishing_short(rawName, lang)
    
    if not response_json:
        return nan,nan

    if 'entities' not in response_json.keys():
        return nan,nan
   
    sorted_entities = sorted(response_json['entities'], key=lambda d: d['confidence_score'], reverse=True)
    for entity in sorted_entities:
        if 'wikidataId' in entity.keys():
            logger.debug('location disambiguated for %s: %s [%s]', rawName, entity['wikidataId'], lang)
            logger.debug('-------------------------------------------------')
            logger.debug(json.dumps(response_json['entities'], indent=4) )
            logger.debug('-------------------------------------------------')
            return entity['wikidataId'], entity['confidence_score']
    
    return nan,nan

LOOKUP_DICT = {}

def lookup_concept(wikidataId):
    """
    Make concept lookup request and process response

    """

    if cfg.USE_CACHE:
        if (wikidataId in LOOKUP_DICT):
            return LOOKUP_DICT[wikidataId]
    
    response_json = wa.request_entity_fishing_concept_lookup(wikidataId)
    
    if not response_json:
        return nan

    if 'statements' not in response_json.keys():
        return nan

    for statement in response_json['statements']:
        if statement['propertyId'] == 'P1566':
            logger.debug('GeoNamesID found for %s: %s', wikidataId,  statement['value'])
            if cfg.USE_CACHE:
                LOOKUP_DICT[wikidataId] = statement['value']
            return statement['value']

 
    return nan

# analysis_df = pd.DataFrame()
# def store_for_analysis(paper_id, part, candidates_df):
#      global analysis_df
    
#      candidates_df.insert(0, 'paper_id', paper_id)
#      candidates_df.insert(1, 'part', part)
    
#      analysis_df =pd.concat([analysis_df, candidates_df  ])
    
#      if (analysis_df.shape[0] % 100):
#          analysis_df.to_csv('geonames_analysis.tsv', sep='\t', encoding='utf-8', index=False)

def annotate_with_geonames(f_json, f_out_json):
    """
    For Wikidata NE generate a list of candidates that can be geographical 
    (Capitalized NE, type = LOCATION). For each candidate make a concept lookup 
    request to entity-fishing. If the response contains a GeoNameID then the candidate is 
    saved as GeoNames NE.
    """
    try:
        ef_json =  read_paper_json(f_json)
        
        annot_json = {}
        annot_json['paper_id'] = ef_json['paper_id']
        
        for part, jpath in cfg.JSON_TEXT_MAP.items():
            entities = get_nested_dict_value(ef_json, [part , 'entities'], default={})
            lang = get_nested_dict_value(ef_json, jpath[1], default=jpath[2])
            
            if entities:
                entities_df = pd.DataFrame.from_records(entities)
                candidates_df = pd.DataFrame()
                if 'wikidataId' in entities_df.columns:
                    candidates_df = entities_df.loc[entities_df['wikidataId'].notna()] \
                                               .loc[entities_df['rawName'].fillna('').str[0].str.isupper()] 
                locations_df = pd.DataFrame()
                if 'type' in entities_df.columns:
                    #try to disambiguate type=LOCATION
                    locations_df =  entities_df.loc[entities_df['type'].fillna('') == 'LOCATION']
                    locations_df[['wikidataId', 'confidence_score']] = list(locations_df['rawName'].apply(disambiguate_location, lang=lang))
                    locations_df = locations_df.loc[locations_df['wikidataId'].notna()] 
                
                candidates_df = pd.concat([candidates_df,
                                           locations_df ]).fillna('')
                
                
                if candidates_df.shape[0] > 0:
                   # Look up concepts for GeoNames ID
                   candidates_df['GeoNamesID'] = candidates_df['wikidataId'].apply(lookup_concept)
                   geonames_df = candidates_df.loc[candidates_df['GeoNamesID'].notna()] 
                   
                   #store_for_analysis(annot_json['paper_id'], part,candidates_df)
         
                   if geonames_df.shape[0] > 0:
                       annot_json[part] = ef_json[part]
                       annot_json[part].pop('global_categories', None)
                       annot_json[part]['date'] = str(datetime.datetime.now())
                       # assign entities
                       annot_json[part] ['entities'] = geonames_df.to_dict(orient='records')


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
    
    f_out = annotate_with_geonames(f_json, f_out)
    logger.info(f_out)
    
    return f_out

#%%    
def annotate_documents(asynch=False):
    """
    Loop through or asynchronously process the Entity-fishing output files 

    """
   
    files = glob.glob(os.path.join(cfg.INPUT_PATH, cfg.INPUT_PATTERN))
    logger.info('found %d files with pattern %s', len(files), cfg.INPUT_PATTERN) 
    
    if asynch:
       with concurrent.futures.ThreadPoolExecutor(max_workers=cfg.ASYNCH_MAX_WORKERS) as executor:
           executor.map(annotate_one, files)
           
    else:       
        for f_json in files:
            annotate_one(f_json)
            
    
    return

#%%     
if __name__ == '__main__':
    # Create output directories
    os.makedirs(cfg.OUTPUT_PATH, exist_ok=True)
        
    annotate_documents(cfg.ASYNCH_PROCESSING)
        
close_timestamp_logger(logger)       

#analysis_df.to_csv('geonames_analysis.tsv', sep='\t', encoding='utf-8', index=False)