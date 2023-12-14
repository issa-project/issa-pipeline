# -*- coding: utf-8 -*-
"""
Download metadata from OAI 2.0 PMH API. Save results as a TSV file.


Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""
import xml.etree.ElementTree as ET
import pandas as pd
import re
import requests
from retrying import retry

import os
import sys

sys.path.append('..') 
from util import read_metadata, save_metadata
from util import open_timestamp_logger, close_timestamp_logger, INFO, DEBUG
from util import detect_lang
from util import add_path_to_config  

add_path_to_config()
from config import cfg_download_corpus_metadata as cfg

#%% Set up logging
logger = open_timestamp_logger( log_prefix= os.path.splitext(os.path.basename(__file__))[0],
                                log_dir=cfg.LOG_PATH,
                                first_line = 'Downloading dataset from OAI API set %s...' % cfg.OAI_DATASET_NAME)

#%% Test OAI API connection
def quick_test():
    """
    Test OAI API connection by requesting the first page of data 

    Parameters: None
    
    Returns: 
        response.text : response HTML 
    """
    headers = {'User-Agent': '%s' % cfg.USER_AGENT }
    response = requests.get(cfg.OAI_ENDPOINT_START % cfg.OAI_DATASET_NAME,
                            verify=True ,
                            headers=headers)
    return response.text

#%% Download data page from OAI-PMH API
@retry(stop_max_delay=10000, wait_random_min=1000, wait_random_max=2000)
def call_oai_api(resumption_token):
    """
    Request page of data from the OAI-PMH API

    Parameters:
        resumption_token : object (first page) or string or xml.etree.ElementTree.Element
        token returned by previous request.

    Returns:
        response_xml : response text as XML string
        resumption_token : xml.etree.ElementTree.Element token for requesting the next page
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

    if isinstance(resumption_token, ET.Element):
        resumption_token = resumption_token.text

    return response_xml, resumption_token

#%% Parse XML response
def xml_to_DataFrame(response_xml):
    """
    Parse XML response from OAI-PMH API into a DataFrame

    Parameters:
        response_xml : response text as XML string

    Returns:
        df : pd.DataFrame of parsed results
    """
    df = pd.DataFrame(columns=list(cfg.SINGLE_FIELD_MAP.keys()) + list(cfg.MULTI_FIELD_MAP.keys()))
    
    for record in response_xml.findall('oai:ListRecords/oai:record', cfg.OAI_NS):

        field_dict = {}

        #read single value fields
        for (col, xpath) in cfg.SINGLE_FIELD_MAP.items():
            try:
                field_dict[col] = record.find(xpath, cfg.OAI_NS).text

                #create a column to hold value of an attribute if it was used in a path
                if field_dict[col] and ('@' in xpath):
                    attr = re.search(r"\[@([^=\]]+)", xpath).group(1)
                    attr = attr.split(':')[-1]
                    field_dict[col+'_'+attr] = list(record.find(xpath, cfg.OAI_NS).attrib.values())[0]

            except:
                pass
            
        #read multiple values fields and create a list out of them    
        for (col, xpath) in cfg.MULTI_FIELD_MAP.items():
            try:
                field_dict[col] = [elem.text for elem in record.findall(xpath, cfg.OAI_NS)]

                #create a column to hold value of an attribute if it was used in a path
                if  ('@' in xpath):
                    #create a column to hold the value of an attribute that was used in a path
                    attr = re.search(r"\[@([^=\]]+)", xpath).group(1)
                    attr = attr.split(':')[-1]

                    field_dict[col+'_'+attr] = [list(elem.attrib.values())[0] for elem in record.findall(xpath, cfg.OAI_NS)]

                    #field_dict[col] = { list(elem.attrib.values())[0] : elem.text for elem in record.findall(xpath, cfg.OAI_NS)}

                    #field_dict[col] = [ (elem.text,list(elem.attrib.values())[0] )  for elem in record.findall(path, NS)]

            except:
                pass

        df = pd.concat([df, pd.DataFrame([field_dict]) ], axis=0, ignore_index=True)

    return df

#%% Downloading data loop from OAI-PMH API
def download_metadata():
    """
    Downloads dataset from OAI 2.0 PMH API 

    Parameters: None 

    Returns:
        df : pd.DataFrame of parsed results
    """
    df = pd.DataFrame()#(columns=list(cfg.SINGLE_FIELD_MAP.keys()) + list(cfg.MULTI_FIELD_MAP.keys()))
    
    resumption_token = object
    
    while (resumption_token is not None):
      
        try:
            response_xml, resumption_token = call_oai_api(resumption_token)
            
        except:
            logger.exception('OAI API call error:')
            break
       
        df_page = xml_to_DataFrame(response_xml)
        df = pd.concat([df, df_page], axis=0, ignore_index=True)
       
        metadata_file = os.path.join(cfg.OUTPUT_PATH, cfg.RAW_DATA_FILENAME)
        save_metadata(df, metadata_file)
        logger.info('Dataset size = %d, saved in %s' % (df.shape[0], metadata_file) )
        
        if cfg.DEBUG:
            break
    
    return df
       
#%%  Main 
# This is the main processing loop that is called from the command line
if __name__ == '__main__':
    download_metadata()

close_timestamp_logger(logger)    
    
