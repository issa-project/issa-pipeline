# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""
import xml.etree.ElementTree as ET
import pandas as pd
import requests
from retrying import retry

import os
import sys

sys.path.append('..')

from config import cfg_download_agritrop_metadata as cfg
from util import open_timestamp_logger, close_timestamp_logger
from util import save_metadata

#%%
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0],
                          log_dir=cfg.LOG_PATH,
                          first_line = 'Download dataset from Agritrop OAI API...')

#%%
def quick_test():
    """
    Test Agritrop OAI API connection by requesting the first page of data 

    Returns
    -------
    String
        Response HTML.

    """
    headers = {'User-Agent': '%s' % cfg.USER_AGENT }
    response = requests.get(cfg.OAI_ENDPOINT_START % cfg.OAI_DATASET_NAME,
                            verify=True ,
                            headers=headers)
    return response.text

#%%
@retry(stop_max_delay=10000, wait_random_min=1000, wait_random_max=2000)
def call_oai_api(resumption_token):
    """
    Request page of data from the Argitrop OAI API

    Parameters
    ----------
    resumption_token : object (first page) or string or xml.etree.ElementTree.Element
        token returned by previous request.

    Returns
    -------
    response_xml : string
        Response text as XML string
    resumption_token : xml.etree.ElementTree.Element
        tocken for requesting the next page
    """
    
    oai_api_url = cfg.OAI_ENDPOINT_START % cfg.OAI_DATASET_NAME
    
    if isinstance(resumption_token, ET.Element):
        oai_api_url = cfg.OAI_ENDPOINT_CONTINUE % resumption_token.text
    
    if isinstance(resumption_token, str):
        oai_api_url = cfg.OAI_ENDPOINT_CONTINUE % resumption_token
            
    headers = {'User-Agent': '%s' % cfg.USER_AGENT }
    logger.info('Calling OAI API: %s', oai_api_url)
    
    response = requests.get(oai_api_url, verify=True, headers=headers)    
    response_xml = ET.fromstring(response.text)
    resumption_token = response_xml.find('oai:ListRecords', cfg.OAI_NS).find('oai:resumptionToken', cfg.OAI_NS)
    
    return response_xml, resumption_token

def download():
    """
    Downloads dataset from Agritrop via OAI 2.0 API either French or English 

    Returns
    -------
    df : pd.DataFrame
        Parsed results
    """
    df = pd.DataFrame(columns=list(cfg.SINGLE_FIELD_MAP.keys()) + list(cfg.MULTI_FIELD_MAP.keys()))
    
    resumption_token = object
    
    while (resumption_token is not None):
      
        try:
            response_xml, resumption_token = call_oai_api(resumption_token)
            
        except:
            logger.exception('OAI API call error:')
            break
        
        for record in response_xml.findall('oai:ListRecords/oai:record', cfg.OAI_NS):
    
            field_dict = {}
    
            #read single value fields
            for (col, path) in cfg.SINGLE_FIELD_MAP.items():
                try:
                    field_dict[col] = record.find(path, cfg.OAI_NS).text
                except:
                    pass
                
            #read multiple values fields and create a list out of them    
            for (col, path) in cfg.MULTI_FIELD_MAP.items():
                try:
                    field_dict[col] = [elem.text for elem in record.findall(path, cfg.OAI_NS)]
                except:
                    pass
    
            df = df.append(field_dict, ignore_index=True)
       
        metadata_file = os.path.join(cfg.OUTPUT_DATASET_PATH, cfg.RAW_DATA_FILENAME)
        save_metadata(df, metadata_file)
        logger.info('Dataset size = %d, saved in %s' % (df.shape[0], metadata_file) )
        
        if cfg.DEBUG:
            break
    
    return df
       
#%%     

if __name__ == '__main__':
    download()

#%%    
close_timestamp_logger(logger)    
    
