# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:38:46 2021

@author: abobashe, Andon Tchechmedjiev 
"""
import os
import sys
import glob
import time
import threading

import requests
from retrying import retry

from lxml import etree
from lxml.etree import XMLSyntaxError
import re
import json
import copy

sys.path.append('..')  
from util import open_timestamp_logger, close_timestamp_logger, INFO, DEBUG
from util import set_nested_dict_value, get_nested_dict_value
from util import copy_file
from util import detect_lang
from util import add_path_to_config  

add_path_to_config()
from config import cfg_extract_text_from_pdf as cfg

#%% Set up logging
logger = open_timestamp_logger(log_prefix=os.path.splitext(os.path.basename(__file__))[0],
                                   file_level=DEBUG if cfg.DEBUG else INFO,
                                   log_dir=cfg.LOG_PATH)

#%% Helper functions for XML processing
def get_xml_element(root, element_name_or_path)->list:
    """
    Retrieve an xml element by path mapped in the cfg.XML_DICT_MAP

    Parameters:
        root : lxml.etree.ElementTree, root of the xml tree
        element_name_or_path : string, name of the element or path to the element

    Returns:
        list of lxml.etree.ElementTree, list of elements
    """
    
    if element_name_or_path.startswith('//'):
        return root.xpath(element_name_or_path, namespaces=cfg.TEI_NS)
    else:
        return root.xpath(cfg.XML_DICT_MAP[element_name_or_path][0], namespaces=cfg.TEI_NS)

def get_first_text (root, element_name_or_path)->str:
    """
    Return text of the first item of the list of items for the path.
    Useful for retrieving an abstract and title.

    Parameters:
        root : lxml.etree.ElementTree, root of the xml tree
        element_name_or_path : string, name of the element or path to the element

    Returns:
        string, text of the first item of the list of items for the path
    """
    
    text_list = get_xml_element(root, element_name_or_path)
    
    if text_list:
        if isinstance(text_list[0],  str):
            return str(text_list[0])
        else:
            return text_list[0].text
        
    return ''    

def get_all_text_as_list (root, element_name_or_path)->list:
    """
    Return all of the items for the xml path as list. 

    Parameters:
        root : lxml.etree.ElementTree, root of the xml tree
        element_name_or_path : string, name of the element or path to the element

    Returns:
        list of strings, text of all the items of the list for the path

    """
   
    text_list = get_xml_element(root, element_name_or_path)
    
    if text_list:
        if isinstance(text_list, str):
            text_list = [text_list]
            
        if not isinstance(text_list[0], str):
            #take only the text of the XML element
            text_list = [t.text for t in text_list] 
            
        #get rid of empty strings before creating final list
        text_list = [t for t in list(map(str.strip, text_list)) if t]            
            
    return text_list  

def get_all_text_as_one (root, element_name_or_path, sep=os.linesep)->str:
    """
    Return concatenated text of all the items of the list for the path.

    Parameters:
        root : lxml.etree.ElementTree, root of the xml tree
        element_name_or_path : string, name of the element or path to the element   
        sep : string, separator between the items of the list

    Returns:
        string, concatenated text of all the items of the list for the path
        
    """
    text_list = get_all_text_as_list(root, element_name_or_path)
            
    return sep.join(text_list)  

#%% Helper functions for language detection
def detect_lang_wrapper(text):
    """
    Wrapper around the utility function to detect language according to the config.

    Parameters:
       text : string, text to detect language for

    Returns:
        string, language code   
    """
    #hint = cfg.DEFAULT_LANGUAGE if cfg.DEFAULT_LANGUAGE != 'en' else None
    bf = cfg.BEST_EFFORT_LANG_DETECTION
    lang, score = detect_lang(text, 
                              best_effort=bf, #hint_language=hint, 
                              return_score=True, logger=logger )
    return lang, score

def detect_language(pdf_dict):
    """
    Detect language of title, abstract and body text and add it to the metadata.

    Parameters:
       pdf_dict : dict, json dictionary with the data       

    Returns:
        dict, json dictionary with the data and language metadata
    """
    
    #detect title language
    lang, score = detect_lang_wrapper(pdf_dict['metadata']['title'])
    set_nested_dict_value(pdf_dict, ['metadata' , 'title_lang'], {'code': lang, 'score': score})

    
    #detect abstract language
    lang, score = detect_lang_wrapper(pdf_dict['abstract'][0]['text'])
    set_nested_dict_value(pdf_dict, ['metadata' , 'abstract_lang'], {'code': lang, 'score': score})
    
    #detect body text language
    if cfg.MERGE_BODY_TEXT:
        text = pdf_dict['body_text'][0]['text']
    else:
        text_list = pdf_dict['body_text']
        text_list = [d['text'] for d in text_list]
        text = os.linesep.join(text_list)
    lang, score = detect_lang_wrapper(text)
    set_nested_dict_value(pdf_dict, ['metadata' , 'body_lang'], {'code': lang, 'score': score})
    
    return pdf_dict
#%% Helper functions for text processing
def replace_doublequotes(text):
    """
    Replace double quotes in string. Double quotes cause problems in conversion to RDF.

    Parameters:
         text : string, text to replace double quotes in

    Returns:
        string, text with double quotes replaced by single quotes
    """
    if isinstance(text, str):
        return text.replace('""' , "'")
    
    if isinstance(text, list):
        if len(text) == 0:
            return text
        
        if isinstance(text[0], str):
            return [ x.replace('""' , "'") for x in text ]
        
        if isinstance(text[0], dict):
            for x in text:
                for k in x:
                    if isinstance(x[k], str):
                        x[k] = x[k].replace('""' , "'")
            return text
    
def dict_to_text(pdf_dict):
    """
    Concatenate title, abstract and body as plain text separated by EOL

    Parameters:
        pdf_dict : dict, json dictionary with the data

    Returns:
        string, concatenated text of title, abstract and body
    """
    text_list = []
    for key, (_, path) in cfg.XML_DICT_MAP.items():
        text = get_nested_dict_value(pdf_dict, path)
        if isinstance(text, list):
            text_list = text_list + [ t['text'] for t in text ]
        elif isinstance(text, str):
            text_list = text_list + [text]
            
    text_list = list(filter(None, text_list))
    text = os.linesep.join(text_list)
    return text
    
#%% Global variables and helper functions for pdf processing

# This global asynchronous timer helps taking the time of processing  
# a pdf into account of a delay time between pdf downloads.
# Delay between pdf downloads prevents blacklisting. 
TIMER = threading.Thread()
TIMER.start()

# Using set of strings is the quickest option to check if file exists
PDF_FILES = set([os.path.basename(f) for f in glob.glob('%s/**/*.pdf' % (cfg.DATASET_ROOT_PATH), recursive = True)] )

@retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=10, wait_random_max=2000)
def download_pdf(pdf_url):
    """
    Download pdf file from a source portal. Support global pdf cache storage and 
    dataset storage.
    
    Parameters:
        pdf_url : string, either url to pdf or file containing url to pdf with extension url

    Returns:
        pdf_path : string, path to the downloaded pdf file
    """
  
    filename = pdf_url.split('/')[-1]
    pdf_path, pdf_content = None, None
    
    if pdf_url.endswith('.url'):
        #this is a path to url file
        filename = os.path.basename(pdf_url).replace('.url', '.pdf')
        with open(pdf_url, 'r') as url_file:
            pdf_url = url_file.read().strip()
   
    elif not pdf_url.startswith('http'):
        raise requests.InvalidURL

    is_new = False
    if cfg.CACHE_PDF:    
        pdf_path = os.path.join(cfg.CACHE_PATH , filename)

        #lookup in cache
        is_new = not os.path.exists(pdf_path)
    else:
        pdf_path = os.path.join( cfg.FILES_LOC['pdf'] , filename)
        
        #lookup in the current dataset
        is_new = filename not in PDF_FILES
 
    global TIMER
    TIMER.join(cfg.DOWNLOAD_DELAY)
    if is_new:
        headers = {'User-Agent': '%s' % cfg.USER_AGENT }

        pdf = requests.get(pdf_url, verify=True , headers=headers)
        pdf_content = pdf.content

        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(pdf_content)
        
        #time.sleep(cfg.DOWNLOAD_DELAY)

    delay = [cfg.DOWNLOAD_DELAY] if is_new else [0.001]
    TIMER = threading.Thread( name='download timer', target=time.sleep, args=delay)
    TIMER.start()
        
   
    return pdf_path, pdf_content

@retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=10, wait_random_max=2000)
def pdf_to_xml(pdf_path, pdf_content=None):
    """
    Convert pdf file to xml string using Grobid API.

    Parameters:
        pdf_path : string, path to the pdf file
        pdf_content : binary stream, previously read pdf_content

    Returns:
        xml : string, xml string with the extracted data
    """
    if not pdf_content:
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as pdf_file:
                pdf_content = pdf_file.read()

    xml = requests.post(cfg.GROBID_API_URL, files={'input': pdf_content}, timeout=cfg.GROBID_TIMEOUT)
    
    return xml.text 

def xml_to_dict(paper_id, xml):
    """
    Extract the data from xml format and represent it as nested dictionary 
    that can be dumped as json. 
    Extracted elements: title, abstract, body text, authors   

    Parameters:
        paper_id : string, paper id
        xml : string, xml string with the extracted data

    Returns:
        output_dict : dict, json dictionary with the data
    """
    # pattern of xml tag
    pattern = re.compile(r'<\?xml.*\?>')
    # replace all the matching xml tag by ''
    xml = pattern.sub('', xml)
            
    root = etree.fromstring(xml)#, base_url=cfg.TEI_BASE_URL)
   
    output_dict = copy.deepcopy(cfg.OUTPUT_SCHEMA.copy())
    output_dict['paper_id'] = paper_id
    
    #title
    xml_path, json_path =  cfg.XML_DICT_MAP['title']
    title = get_first_text(root, xml_path)
    if title:
        title = replace_doublequotes(title)
        set_nested_dict_value(output_dict, json_path, title)
    
    #abstract     
    xml_path, json_path =  cfg.XML_DICT_MAP['abstract']        
    abstract = get_all_text_as_one(root, xml_path, sep=' ')
    if abstract:
        abstract = replace_doublequotes(abstract)
        set_nested_dict_value(output_dict, json_path, abstract)
        
    #keywords
    xml_path, json_path =  cfg.XML_DICT_MAP['keywords']
    keywords = get_all_text_as_one(root, xml_path, sep=', ')
    #keywords = get_all_text_as_list(root, xml_path)

    if keywords:
        keywords = replace_doublequotes(keywords)
        set_nested_dict_value(output_dict, json_path, keywords)
    
    #body
    xml_path, json_path =  cfg.XML_DICT_MAP['body_text']  
    if cfg.MERGE_BODY_TEXT:
        body = [{'text': get_all_text_as_one(root, xml_path, sep=cfg.MERGE_SEPARATOR)}]     
    else:
        body = [{'text': t} for t in get_all_text_as_list(root, xml_path) ]     

    if body:
        body = replace_doublequotes(body)
        set_nested_dict_value(output_dict, json_path, body)

    return output_dict


#%%
def process_pdf(pdf_file_path, json_file_path, 
                               pdf_content=None,
                               xml_file_path=None,
                               text_file_path=None,):
    """
    Processing pipeline: call Grobid for PDF -> 
                         parse XML to JSON according to the schema -> 
                         (optionally) detect text language -> 
                         save JSON ->
                         (optionally) save intermediate XML ->
                         (optionally) save plain text file

    Parameters:
        pdf_file_path : string, input PDF file path.
        json_file_path: string, optional output json file. 
        pdf_content: binary stream, previously read pdf_content    
        xml_file_path string, optional file path for Grobid output XML. The default is None.
                        If not specified and config.SAVE_XML=true it would be created from the
                        repository configuration for the xml output file and pdf file name.
                        Otherwise it would not be saved.
        text_file_path string, optional file path for plain text. The default is None.
                        If not specified and config.SAVE_TEXT=true it would be created from the
                        repository configuration for the txt output file and pdf file name  
                        Otherwise it would not be saved.

    Returns:
        json_file_path : string, resulting file path
        pdf_dict : dict, resulting json dictionary
    """
    pdf_dict = cfg.OUTPUT_SCHEMA if cfg.OUTPUT_IF_BAD_PDF else {}
    xml = ''
    
    #text extraction
    try:
        paper_id = os.path.splitext(os.path.basename(pdf_file_path))[0]

        pdf_dict['paper_id'] = paper_id
      
        xml = pdf_to_xml(pdf_file_path, pdf_content=pdf_content)
        
        pdf_dict = xml_to_dict(paper_id, xml)
        
        if cfg.DETECT_LANG:
            pdf_dict = detect_language(pdf_dict)
        
    except XMLSyntaxError:
        copy_file(pdf_file_path, cfg.CACHE_UNREADABLE_PATH)
        
        logger.error('Cannot extract text from pdf, perhaps this is a scanned document.')
       
    #saving results
    try: 
        if json_file_path and pdf_dict:
            with open(json_file_path, 'w' , encoding='utf-8') as json_file:
                json.dump(pdf_dict, json_file, indent=4, ensure_ascii=False)
                
        if cfg.SAVE_XML:
            if not xml_file_path:
                xml_file_path = os.path.join(cfg.OUTPUT_XML_PATH, paper_id + cfg.OUTPUT_SUFFIX +'.xml')     
                #xml_file_path = os.path.realpath(os.path.normpath(xml_file_path))
        
        if cfg.SAVE_TEXT:
            if not text_file_path:
                text_file_path = os.path.join(cfg.FILES_LOC['txt'], paper_id + cfg.OUTPUT_SUFFIX +'.txt')     
                #text_file_path = os.path.realpath(os.path.normpath(text_file_path))
     
        if xml_file_path and xml:
            with open(xml_file_path, 'w' , encoding='utf-8') as xml_file:
                xml_file.write(xml)
                
        if text_file_path:
            text = dict_to_text(pdf_dict)
            with open(text_file_path, 'w',  encoding='utf-8') as txt_file:
                txt_file.write(text)
  
    except Exception as e:
        logger.exception(e)


    return json_file_path, pdf_dict

        
def process_all():
    """
    Process all the pdf files in the input directory according to the config.

    """
    pdf_path  = cfg.INPUT_PATH
    json_path = cfg.OUTPUT_PATH
    
    files = glob.fnmatch.filter(os.listdir(pdf_path), cfg.INPUT_PATTERN)
    
    for f_pdf in files:
        f_pdf = os.path.join(pdf_path, f_pdf)
        f_pdf = os.path.realpath(os.path.normpath(f_pdf))
        logger.info(f_pdf + '--->')
         
        f_json = os.path.join(json_path, os.path.basename(f_pdf).split('.')[0] + cfg.OUTPUT_SUFFIX + '.json')
        
        if not cfg.OVERWRITE_EXISTING and os.path.exists(f_json):
            logger.info(f_json + ' already exists')
            continue

        process_pdf(f_pdf, f_json)
        logger.info(f_json)
        
    return

def create_cache():
    """
    Create a dedicated cache location for the PDF files

    """
    if cfg.CACHE_PDF:
        os.makedirs(cfg.CACHE_PATH, exist_ok=True)
    os.makedirs(cfg.CACHE_UNREADABLE_PATH, exist_ok=True) 

def download_and_process_all():
    """
    Download all the pdf files in the input directory according to the config 
    and immediately process each file. The processing occurs while waiting for 
    the next file download.

    """
    create_cache()
    
    url_path  = cfg.INPUT_PATH
    json_path = cfg.OUTPUT_PATH
    
    files = glob.fnmatch.filter(os.listdir(url_path), cfg.INPUT_PATTERN)
    logger.info('found %d files in %s with pattern %s', len(files), url_path, cfg.INPUT_PATTERN) 

    for f_url in files:
        
        try:
            f_url = os.path.join(url_path, f_url)
            logger.info(f_url + '--->')
            
            f_pdf, pdf_content = download_pdf(f_url)
            if not pdf_content:
                logger.info(f_pdf + ' already exists')
            else:    
                logger.info(f_pdf + '--->')
             
            f_json = os.path.join(json_path, os.path.basename(f_url).split('.')[0] + cfg.OUTPUT_SUFFIX + '.json')
            
            if not cfg.OVERWRITE_EXISTING and os.path.exists(f_json):
                logger.info(f_json + ' already exists')
                continue
    
            process_pdf(f_pdf, f_json, pdf_content=pdf_content)
            
            logger.info(f_json)
        except Exception as e:
            logger.exception(e)
        
    return

#%% Main
if __name__ == '__main__':

    if cfg.INPUT_PATTERN.endswith('pdf'):
        process_all()
    elif cfg.INPUT_PATTERN.endswith('url'):
       download_and_process_all()

close_timestamp_logger(logger)