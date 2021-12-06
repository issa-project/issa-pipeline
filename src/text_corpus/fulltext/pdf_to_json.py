# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:38:46 2021

@author: abobashe, Andon Tchechmedjiev 
"""
import os
import sys
import glob

import requests
from retrying import retry

from lxml import etree
from lxml.etree import XMLSyntaxError
import re

import json

sys.path.append('..')  

from config import cfg_pdf_to_json as cfg
from util import detect_lang
from util import open_timestamp_logger, close_timestamp_logger
from util import set_nested_dict_value
from logging import INFO, DEBUG
#%% 
if len(sys.argv) > 1 :    
    # if arguments are specified it means that this script is called for just 
    # one pdf file and most likey the log will be captured by redirection from the calling script
    logger = open_timestamp_logger(log_prefix=None, #os.path.splitext(os.path.basename(__file__))[0] if cfg.DEBUG else None ,
                                   console_level=INFO if cfg.DEBUG else DEBUG,
                                   log_dir=cfg.LOG_PATH)
else:
    #if no agrguments were specified then initialise the timed log file
    logger = open_timestamp_logger(log_prefix=os.path.splitext(os.path.basename(__file__))[0],
                                   console_level=INFO if cfg.DEBUG else DEBUG,
                                   log_dir=cfg.LOG_PATH)


#%%
def get_xml_element(root, element_name_or_path):
    """
    Retrievan xml elemnt by path mapped in the cfg.XML_DICT_MAP

    Parameters
    ----------
    root : lxml....
        root xml element
    element_name : str
        key in cfg.XML_DICT_MAP 

    Returns
    -------
    lxml.Element
        
    """
    
    if element_name_or_path.startswith('//'):
        return root.xpath(element_name_or_path, namespaces=cfg.TEI_NS)
    else:
        return root.xpath(cfg.XML_DICT_MAP[element_name_or_path][0], namespaces=cfg.TEI_NS)

def get_first_text (root, element_name_or_path):
    
    text_list = get_xml_element(root, element_name_or_path)
    
    if text_list:
        if isinstance(text_list[0],  str):
            return str(text_list[0])
        else:
            return text_list[0].text
        
    return ''    

def get_all_text_as_list (root, element_name_or_path):
    
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

def get_all_text_as_one (root, element_name_or_path, sep=os.linesep):
    
    text_list = get_all_text_as_list(root, element_name_or_path)
            
    return sep.join(text_list)  


# def set_nested_dict_value(nested_dict, element, value):
#     """
#     Assign value to a mapped  keys in the nested dictionalry 

#     Parameters
#     ----------
#     nested_dict : dict

#     element : key in cfg.XML_DICT_MAP or list of keys an indices

#     value : any type
        

#     Returns
#     -------
#     nested_dict : dict
#         updated dictionary

#     """
#     #TODO:refactor
#     if isinstance(element , str):
#         path = cfg.XML_DICT_MAP[element][1]
#     else:
#         path = element
    
#     val = nested_dict
#     for k in path[:-1]:
#         val = val[k] 
    
#     val[path[-1]] = value 
    
#     return nested_dict

#%%
def format_body(text_list):
    """
    Format a body text accoding to the configuration
    Parameters
    ----------
    text_list : list of strings | list of of lxml.etree.Element | string
        list of XML elements representing text fragments

    Returns
    -------
    list
        list of text dictionaries to be saved as json 
        or one text dictionary that contains merged text 
        depending on the MERGE_BODY_TEXT flag in config

    """ 
       
    if cfg.MERGE_BODY_TEXT:
        return [{'text': cfg.MERGE_SEPARATOR.join(text_list)}]
        
    return [{'text': t} for t in text_list ]

#TODO: mapping
def format_author(el):
    """
    Format authors according to the JSON schema adapted from CORD-19

    Parameters
    ----------
    el : TYPE
        DESCRIPTION.

    Returns
    -------
    author : TYPE
        DESCRIPTION.

    """
    author = {}

    first = el.xpath('.//tei:persName/tei:forename[@type="first"]/text()[1]', namespaces=cfg.TEI_NS)
    if first:
        author['first'] = first[0] + ('.' if len(first[0])==1 else '')

    middle = el.xpath('.//tei:persName/tei:forename[@type="middle"]', namespaces=cfg.TEI_NS)
    if middle:
        author['middle'] = [m.text + ('.' if len(m.text)==1 else '') for m in middle]


    last = el.xpath('.//tei:persName/tei:surname/text()', namespaces=cfg.TEI_NS)
    if last :
       author['last'] = last[0]

    affiliation = {}
    for aff in el.xpath('.//tei:affiliation', namespaces=cfg.TEI_NS):
        institution = aff.xpath('.//tei:orgName[@type="institution"][1]/text()', namespaces=cfg.TEI_NS)
        affiliation ['institution'] = institution[0] if  institution else ''

        affiliation ['location'] = {}
        settlement = aff.xpath('.//tei:address/tei:settlement[1]/text()',  namespaces=cfg.TEI_NS)
        affiliation ['location']['settlement'] = settlement[0] if settlement else ''

        country = aff.xpath('.//tei:address/tei:country[1]/text()', namespaces=cfg.TEI_NS)
        affiliation ['location']['country'] = country[0] if country else ''
        
        #remove empty elements
        affiliation ['location'] = {k: v for k, v in affiliation['location'].items() if v}

    #remove empty elements    
    affiliation = {k: v for k, v in affiliation.items() if v}
    
    author['affiliation'] = affiliation

    author = {k: v for k, v in author.items() if v}

    return author

#%%
#TODO: fininsh
def element_to_reference(el):
    result = {}

    result['ref_title'] = extract_reference_title(el)

    result['authors'] = [
        format_author(e) for e in el.xpath('.//tei:author', namespaces=cfg.TEI_NS)
    ]

    result['journal_pubnote'] = extract_reference_pubnote(el)

    return result


def extract_reference_title(el):
    title = el.xpath('.//tei:analytic/tei:title[@level="a" and @type="main"]', namespaces=cfg.TEI_NS)
    if title and len(title) == 1:
        return title[0].text


def extract_reference_pubnote(el):
    result = {}

    journal_title = el.xpath('./tei:monogr/tei:title', namespaces=cfg.TEI_NS)
    if journal_title and len(journal_title) == 1:
        result['journal_title'] = journal_title[0].text

    journal_volume = el.xpath(
        './tei:monogr/tei:imprint/tei:biblScope[@unit="volume"]',
        namespaces=cfg.TEI_NS
    )
    if journal_volume and len(journal_volume) == 1:
        result['journal_volume'] = journal_volume[0].text

    journal_issue = el.xpath(
        './tei:monogr/tei:imprint/tei:biblScope[@unit="issue"]',
        namespaces=cfg.TEI_NS
    )
    if journal_issue and len(journal_issue) == 1:
        result['journal_issue'] = journal_issue[0].text

    year = el.xpath(
        './tei:monogr/tei:imprint/tei:date[@type="published"]/@when',
        namespaces=cfg.TEI_NS
    )
    if year and len(year) == 1:
        result['year'] = year[0]

    pages = []

    page_from = el.xpath(
        './tei:monogr/tei:imprint/tei:biblScope[@unit="page"]/@from',
        namespaces=cfg.TEI_NS
    )
    if page_from and len(page_from) == 1:
        pages.append(page_from[0])

    page_to = el.xpath(
        './tei:monogr/tei:imprint/tei:biblScope[@unit="page"]/@to',
        namespaces=cfg.TEI_NS
    )
    if page_to and len(page_to) == 1:
        pages.append(page_to[0])

    result['page_range'] = '-'.join(pages)

    return result
#%%
def detect_lang_wrapper(text):
    """
    WRapper around the utility function to detect language according to 
    the config

    Parameters
    ----------
    text : string
        Text to be processed

    Returns
    -------
    lang : str
        2-letter language code.
    score : float
        confidence score.

    """
    hint = cfg.DEFAULT_LANGUAGE if cfg.DEFAULT_LANGUAGE != 'en' else None
    bf = cfg.BEST_EFFORT_LANG_DETECTION
    lang, score = detect_lang(text, 
                              best_effort=bf, hint_language=hint, 
                              return_score=True, logger=logger )
    return lang, score

def detect_language(pdf_dict):
    
    
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
#%%
@retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=10, wait_random_max=2000)
def pdf_to_xml(pdf_path):
    """
    Convert pdf file to xml string using Grobid API.

    Parameters
    ----------
    pdf_path : string
         PDF file path.

    Returns
    -------
    string
        Response xml

    """
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            pdf_content = pdf_file.read()

    # http://localhost:8070
    url = cfg.GROBID_API_URL

    xml = requests.post(url, files={'input': pdf_content})
    
    return xml.text 

#%%
def xml_to_dict(paper_id, xml):
    """
    Extract the data from xml format and represent it in nested dictionary 
    that can be dumped as json. 
    Extracted elements: title, abstract, body text, authors   

    Parameters
    ----------
    paper_id : string
        id of the parsed document.
    xml : str
        extracted xml.

    Returns
    -------
    output_dict : dict
        nested dictionary representing output json

    """
    # pattern of xml tag
    pattern = re.compile(r'<\?xml.*\?>')
    # replace all the matching xml tag by ''
    xml = pattern.sub('', xml)
            
    root = etree.fromstring(xml)#, base_url=cfg.TEI_BASE_URL)
   
    output_dict = cfg.OUTPUT_SCHEMA.copy()
    output_dict['paper_id'] = paper_id
    
    #title 
    title = get_first_text(root, 'title')
    if title:
        #output_dict['metadata']['title'] = title[0].text
        #set_nested_dict_value(output_dict, 'title', title)
        set_nested_dict_value(output_dict, cfg.XML_DICT_MAP['title'][1], title)
        
    #abstract 
    abstract = get_all_text_as_one(root, 'abstract', sep=' ')
    if abstract:
        #output_dict['abstract'] = format_abstract(abstract)
        #set_nested_dict_value(output_dict, 'abstract', format_abstract(abstract))
        #set_nested_dict_value(output_dict, 'abstract', abstract)
        set_nested_dict_value(output_dict, cfg.XML_DICT_MAP['abstract'][1], abstract)
    
    #body
    body = get_all_text_as_list(root, 'body_text')
    if body:
        #output_dict['body_text'] = format_body(body)
        #set_nested_dict_value(output_dict, 'body_text', format_body(body))
        set_nested_dict_value(output_dict, cfg.XML_DICT_MAP['body_text'][1], format_body(body))

    #authors
    if cfg.INCLUDE_AUTHORS: 
        authors = get_xml_element(root, 'authors')
        if authors:
            set_nested_dict_value(output_dict, ['metadata','authors'], list(map(format_author, authors)))
            
            #output_dict['metadata']['authors'] = list(map(format_author, authors))
        
    #Bibliography
    #if cfg.INCLUDE_BIB:
        
    #references = get_xml_element(root, 'bib_entries')
    #if references:
    #    output_dict['ref_entries'] =  list(map(element_to_reference, references))


    return output_dict
#%%
def dict_to_text(pdf_dict):
    """
    Concatenate title, abstract and body as plain text separateed by EOL 

    Parameters
    ----------
    pdf_dict : dict
        json representation

    Returns
    -------
    text : str
        concatenated text

    """
    text = os.linesep.join([  pdf_dict['metadata']['title'],
                              pdf_dict['abstract'][0]['text'],
                              ] + 
                              [ bt['text'] for bt in pdf_dict['body_text'] ] ) 
    
    return text


#%%
def process_pdf(pdf_file_path, json_file_path=None, 
                                      xml_file_path=None,
                                      text_file_path=None):
    """
    Processing pipeline: call Grobid for PDF -> parse XML to JSON according 
    to the schema -> {optionally detect text language} -> save JSON ->
    {optionally save intermediate XML} -> {optionally save plain text file}}}

    Parameters
    ----------
    pdf_file_path : string
        Input PDF file path.
    json_file_path: string, optional
        Optional file path to the output json file. The default is None.
        If not specified it would be created from the repository configuration
        for the json output file and pdf file name  
    xml_file_path string, optional
        Optional file path for Grobid output XML. The default is None.
        If not specified and config.SAVE_XML=true it would be created from the
        repository configuration for the xml output file and pdf file name.
        Otherwise it would not be saved.
    text_file_path string, optional
        Optional file path forplain text. The default is None.
        If not specified and config.SAVE_TEXT=true it would be created from the
        repository configuration for the txt output file and pdf file name  
        Otherwise it would not be saved.

    Returns
    -------
    json_file_path : 
        Resulting file path.
    pdf_dict : dict
        Resulting json dictionary

    """
    paper_id = os.path.splitext(os.path.basename(pdf_file_path))[0]
    
    if not json_file_path:
        json_file_path = os.path.join(cfg.FILES_LOC['fulltext_json'], paper_id + cfg.OUTPUT_SUFFIX + '.json')
        json_file_path = os.path.realpath(os.path.normpath(json_file_path))
        
    if not xml_file_path:
        if cfg.SAVE_XML:
            xml_file_path = os.path.join(cfg.FILES_LOC['xml'], paper_id + cfg.OUTPUT_SUFFIX +'.xml')     
            xml_file_path = os.path.realpath(os.path.normpath(xml_file_path))
            
    if not text_file_path:
        if cfg.SAVE_TEXT:
            text_file_path = os.path.join(cfg.FILES_LOC['txt'], paper_id + cfg.OUTPUT_SUFFIX +'.txt')     
            text_file_path = os.path.realpath(os.path.normpath(text_file_path))    

    logger.info('Paper id: %s', paper_id)
    
    #check if xtraction was done before and/or we want to do it again
    if (not cfg.OVERWRITE_EXISTING) and os.path.exists(json_file_path):
        logger.info('Skipping extraction, using cached file %s', json_file_path)
        return json_file_path, None

    #text extraction
   
    xml = pdf_to_xml(pdf_file_path)
    
    pdf_dict = xml_to_dict(paper_id, xml)
    
    if cfg.DETECT_LANG:
        pdf_dict = detect_language(pdf_dict)
        
    #saving results    
    if json_file_path:
        with open(json_file_path, 'w' , encoding='utf-8') as json_file:
            json.dump(pdf_dict, json_file, indent=4, ensure_ascii=False)

    if xml_file_path:
        with open(xml_file_path, 'w' , encoding='utf-8') as xml_file:
            xml_file.write(xml)
            
    if text_file_path:
        text = dict_to_text(pdf_dict)
        with open(text_file_path, 'w',  encoding='utf-8') as txt_file:
            txt_file.write(text)

    return json_file_path, pdf_dict

def process_one(f_pdf, f_json=None, f_xml=None, f_txt=None):
    try:
         
        f_json, _= process_pdf(f_pdf, f_json, f_xml, f_txt)
        logger.info('Extracted text from %s to %s', f_pdf, f_json)
        
    except XMLSyntaxError:
        logger.error('Cannot extract text from %s, perhaps this is a scanned document.', f_pdf)

    except Exception as e:
        logger.exception(e)
        
def process_all():
    
    pdf_path = cfg.FILES_LOC['pdf']
    
    files = glob.fnmatch.filter(os.listdir(pdf_path), "*.pdf")
    
    for f_pdf in files:
        f_pdf = os.path.join(pdf_path, f_pdf)
        f_pdf = os.path.realpath(os.path.normpath(f_pdf))

        process_one(f_pdf)
    
    return

#%%
import argparse

def _resolve_file(path_string):
    return os.path.realpath(os.path.normpath(os.path.expanduser(path_string))) 
def _resolve_dir(path_string):
    return os.path.realpath(os.path.normpath(os.path.expanduser(os.path.dirname(path_string))))
  
PARSER = argparse.ArgumentParser(description='Extracting text from PDF file with  Grobid')
PARSER.add_argument('--pdf',    help='path to the PDF file' , type=_resolve_file)
PARSER.add_argument('--json', help='optional file path for JSON output, if not specified the configured repository path will be used' , type=_resolve_file)
PARSER.add_argument('--xml', help='optional file path for XML output' , type=_resolve_dir)
PARSER.add_argument('--txt',  help='optional file path for TEXT output' , type=_resolve_dir)

#TODO: add checking reading grobid connection and version
def main():
    
    parsed_arguments   = PARSER.parse_args(sys.argv[1:])
  
    f_pdf = parsed_arguments.pdf
    f_json =  parsed_arguments.json
    f_xml =  parsed_arguments.xml
    f_txt = parsed_arguments.txt
    
    if f_pdf:
        process_one(f_pdf, f_json, f_xml, f_txt)
    else:
        process_all()
    
 
if __name__ == '__main__':
    main()

close_timestamp_logger(logger)