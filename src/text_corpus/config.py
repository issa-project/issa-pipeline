# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 19:14:38 2021

@author: abobashe
"""

# read environment variables defined and exported in env.sh
import os

def read_env_var(var_name):
    return os.environ[var_name] if var_name in os.environ else None

_ISSA_DATA_ROOT  = read_env_var('ISSA_DATA_ROOT') or '../../../data'
_ISSA_DATASET    = read_env_var('ISSA_DATASET') or 'dataset-0-0'
_METADATA_PREFIX = read_env_var('METADATA_PREFIX') or 'metadata'  
_LANG            = read_env_var('DATASET_LANGUAGE') or 'en'

class cfg_download_agritrop_metadata(object):
    LANGUAGE = {'fr': 'fre',
                'en': 'eng'} [_LANG]
    
    OAI_DATASET_NAME = f'issa_{LANGUAGE}' 
    
    OAI_ENDPOINT_START = 'https://agritrop.cirad.fr/cgi/oai2?verb=ListRecords&metadataPrefix=oai_dc&set=%s'
    OAI_ENDPOINT_CONTINUE ='https://agritrop.cirad.fr/cgi/oai2?verb=ListRecords&resumptionToken=%s'
    USER_AGENT = 'ISSA extraction script' 
    
    OAI_NS = {'oai': 'http://www.openarchives.org/OAI/2.0/', 
              'dc' : 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/'}

    
    RAW_DATA_FILENAME = f'{_METADATA_PREFIX}_{_LANG}.raw.tsv'
    OUTPUT_DATASET_PATH = '../output'
    LOG_PATH = '../logs'

    SINGLE_FIELD_MAP = {'agritrop_id' : 'oai:header/oai:identifier',
                         'datestamp' :  'oai:header/oai:datestamp',
                         'uri' : 'oai:metadata/oai_dc:dc/dc:identifier',
                        'title' : 'oai:metadata/oai_dc:dc/dc:title',
                        'language' : 'oai:metadata/oai_dc:dc/dc:language',
                        'year' : 'oai:metadata/oai_dc:dc/dc:date',
                        'abstract' : 'oai:metadata/oai_dc:dc/dc:description',
                        'type' : 'oai:metadata/oai_dc:dc/dc:type',
                        'publication' : 'oai:metadata/oai_dc:dc/dc:source',
                        'pdf_url' : 'oai:metadata/oai_dc:dc/dc:identifier[last()]',
                        'doi': '',
                        'iso_lang': '',
                        'license_text' :'',
                        'license_uri' : '',
                        'title_lang': '',
                        'title_lang_score': '',
                        'abstarct_lang': '',
                        'abtract_lang_score': ''
                        }
    
    MULTI_FIELD_MAP = {'authors' : 'oai:metadata/oai_dc:dc/dc:creator',
                       'descriptors' : 'oai:metadata/oai_dc:dc/dc:subject',
                       'geo_descriptors' : 'oai:metadata/oai_dc:dc/dc:coverage',
                       'agrovoc_uris' :'' ,
                       'agrovoc_labels': '',
                       'identifiers' : 'oai:metadata/oai_dc:dc/dc:identifier',
                       'licenses' : 'oai:metadata/oai_dc:dc/dc:rights',
                       'relations' : 'oai:metadata/oai_dc:dc/dc:relation', #ideally it should have XML path expression [starts-with(.,"http")] butit is not supported
                       'same_as' : '',
                       'identifiers' : 'oai:metadata/oai_dc:dc/dc:identifier',
                       'types' : 'oai:metadata/oai_dc:dc/dc:type',
                      }
    DEBUG = False

#TODO: coordinate with download config    

class cfg_process_agritrop_metadata(object):
    LANGUAGE = _LANG
    
    RAW_DATA_FILENAME = f'{_METADATA_PREFIX}_{_LANG}.raw.tsv'
    PROCESSED_DATA_FILENAME = f'{_METADATA_PREFIX}_{_LANG}.tsv'
    
    INPUT_PATH = '../output'
    OUTPUT_PATH = '../output'
    LOG_PATH = '../logs'
    
    from metadata.agrovoc_wrapper import Agrovoc_Wrapper

    SPARQL_WRAPPER = Agrovoc_Wrapper()
        
    ARGROVOC_QUERY_TEMPLATE = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
    PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
    SELECT ?concept ?label 
    WHERE { 
      VALUES(?concept) {%s}
      
      ?concept a skos:Concept . 
      ?concept skos:prefLabel ?label.
      
      FILTER(langMatches(lang(?label), '%s')) 
    }  
    '''
    
    BEST_EFFORT_LANG_DETECTION = False
    FILL_NOT_DETECTED_LANG = False

class cfg_create_dataset_repository(object):
    LANGUAGE = _LANG
    
    PROCESSED_DATA_FILENAME = f'{_METADATA_PREFIX}_{_LANG}.tsv'
    
    INPUT_PATH = '../output'
    LOG_PATH = '../logs'
    OUTPUT_ROOT_PATH =  _ISSA_DATA_ROOT
    DATASET_NAME = _ISSA_DATASET

    FILES_LOC = { 'metadata' :  os.path.join(OUTPUT_ROOT_PATH, DATASET_NAME, _LANG),
                 'tsv' :  os.path.join(OUTPUT_ROOT_PATH, DATASET_NAME, _LANG, 'labels' ),
                 'txt' :  os.path.join(OUTPUT_ROOT_PATH, DATASET_NAME, _LANG, 'txt' ),
                 'url' :  os.path.join(OUTPUT_ROOT_PATH, DATASET_NAME, _LANG, 'pdf' ),
                 'pdf' :  os.path.join(OUTPUT_ROOT_PATH, DATASET_NAME, _LANG, 'pdf' ),
                 'metadata_json' : os.path.join(OUTPUT_ROOT_PATH, DATASET_NAME, _LANG, 'json', 'metadata' ),
                 'fulltext_json' : os.path.join(OUTPUT_ROOT_PATH, DATASET_NAME, _LANG, 'json', 'fulltext' ),
                 'coalesced_json' : os.path.join(OUTPUT_ROOT_PATH, DATASET_NAME, _LANG, 'json', 'coalesced' ),
                 'xml' :  os.path.join(OUTPUT_ROOT_PATH, DATASET_NAME, _LANG, 'xml' ),
                 }

    REMOVE_FILES = False
    SAVE_LABELS_TSV = True
    SAVE_PDF_URL = True
    SAVE_TITLE_ABSTRACT_TEXT = False
    SAVE_TITLE_ABSTRACT_JSON = True
    
    JSON_SUFFIX = '.oai'
    
    JSON_SCHEMA={'paper_id' : '',
                   'metadata' : {'title': '',
                               'authors': '',
                               'keywords':'',
                               #'abstract' : '',
                               'title_lang': {'code': '', 'score': 0.0},
                               'abstract_lang': {'code': '', 'score': 0.0},
                               },
                   'abstract' : [{'text' : ''}],
                 }
    
    DATAFRAME_TO_JSON_MAP = {'agritrop_id' : ['paper_id'],
                             'title'       : ['metadata', 'title'],
                             'abstract'    : ['abstract', 0, 'text'],
                             
                             'title_lang'           : ['metadata', 'title_lang','code'] ,
                             'title_lang_score'     : ['metadata', 'title_lang','score'] ,
                             'abstract_lang'        : ['metadata', 'abstract_lang','code'] ,
                             'abstract_lang_score'  : ['metadata', 'abstract_lang','score'] ,
                
        }

    
class cfg_pdf_to_json(object):

    GROBID_URL = 'http://localhost:8070'
    GROBID_API_URL = f'{GROBID_URL}/api/processFulltextDocument'
    
    OUTPUT_ROOT_PATH = _ISSA_DATA_ROOT
    DATASET_NAME = _ISSA_DATASET
    LOG_PATH = '../logs'
    
    SAVE_XML = True
    SAVE_TEXT= False
    MERGE_BODY_TEXT = True
    OVERWRITE_EXISTING = True
    
    TEI_BASE_URL = "http://www.tei-c.org/ns/1.0/"
    TEI_NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    MERGE_SEPARATOR = '\n'
    
    OUTPUT_SCHEMA={'paper_id' : '',
                     'metadata' : {'title': '',
                                   'authors': '',
                                   'title_lang': {'code': '', 'score': 0.0},
                                   'abstract_lang': {'code': '', 'score': 0.0},
                                   'body_lang': {'code': '', 'score': 0.0} },
                     'abstract' : [{'text' : ''}],
                     'body_text': [{'text' : ''},],
                     'ref_entries': ''
                     }
    
    XML_DICT_MAP = {'title':    ('//tei:titleStmt/tei:title//text()', ['metadata', 'title']),
                   'abstract':  ('//tei:profileDesc/tei:abstract//text()' ,  ['abstract' , 0, 'text']),
                   'body_text': ('//tei:body//tei:p[text()]', ['body_text']), # #return root.xpath("//tei:body//tei:p//text()", namespaces=NS) #- more
                   'authors':   ('//tei:fileDesc//tei:author', ['metadata', 'authors']),
                   'bib_entries': ('//tei:text//tei:listBibl/tei:biblStruct', ['bib_entries'])}
    
    OUTPUT_SUFFIX = '.grobid'
    
    DEFAULT_LANGUAGE = _LANG
    DETECT_LANG = True
    BEST_EFFORT_LANG_DETECTION = False
    
    INCLUDE_AUTHORS = False
    INCLUDE_BIB = False


    
    DEBUG=True
    
    # Dependency on the create_dataset-repository config
    FILES_LOC = cfg_create_dataset_repository.FILES_LOC    
    
class cfg_coalesce_meta_json(object):
   
    DO_COALESE = True
    LOG_PATH = '../logs'
    
    JSON_SUFFIX = ''

    # Dependency on the create_dataset-repository config
    FILES_LOC = cfg_create_dataset_repository.FILES_LOC    
    METADATA_FILE = os.path.join(FILES_LOC['metadata']  , f'{_METADATA_PREFIX}_{_LANG}.tsv')
    GROBID_JSON_PATH = FILES_LOC['fulltext_json']
    
    JSON_SCHEMA = cfg_create_dataset_repository.JSON_SCHEMA
    DATAFRAME_TO_JSON_MAP = cfg_create_dataset_repository.DATAFRAME_TO_JSON_MAP
    
    
    