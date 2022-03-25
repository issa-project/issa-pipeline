# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 19:14:38 2021

@author: abobashe
"""

# read environment variables defined and exported in env.sh
import os
import datetime

from  sparql_endpoint_wrapper import SPARQL_Endpoint_Wrapper

def read_env_var(var_name):
    return os.environ[var_name] if var_name in os.environ else None

_ISSA_DATA_ROOT  = read_env_var('ISSA_DATA_ROOT') or '../../data'
_ISSA_DATASET    = read_env_var('ISSA_DATASET') or 'dataset-0-0'
_LATEST_UPDATE    = read_env_var('LATEST_UPDATE') or ''
_METADATA_PREFIX = read_env_var('METADATA_PREFIX') or 'agritrop'  
_LANG            = read_env_var('DATASET_LANGUAGE') or 'en'
_ANNIF_SUFFIX    = read_env_var('ANNIF_SUFFIX') or 'annif'
_PDF_CACHE       = read_env_var('PDF_CACHE') or '../../data/pdf_cache'
_PDF_CACHE_UNREADABLE = read_env_var('PDF_CACHE_UNREADABLE') or '../../data/pdf_cache/unreadable'

class cfg_pipeline(object):
    """
    Shared settings
    
    """

    LOG_PATH = '../logs' 
   
    DATASET_ROOT_PATH = os.path.join(_ISSA_DATA_ROOT, _ISSA_DATASET)
   
    CURRENT_DATE = datetime.datetime.now().strftime('%Y%m%d')
    LATEST_UPDATE = [x for x in (sorted(os.listdir(DATASET_ROOT_PATH), reverse=True) ) ]
                         #    if os.path.isdir( os.path.join(DATASET_ROOT_PATH, x) )] # TODO: check weired behaviour

    LATEST_UPDATE = LATEST_UPDATE[0] if LATEST_UPDATE else CURRENT_DATE

    FILES_LOC = {'metadata' :      os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE),
               'tsv' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'labels' ),
               'txt' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'txt' ),
               'url' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'pdf' ),
               'pdf' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'pdf' ),
               'metadata_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'json', 'metadata' ),
               'fulltext_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'json', 'fulltext' ),
               'coalesced_json' :  os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'json', 'coalesced' ),
               'xml' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'xml' ),
               'indexing_text' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'indexing' ),
               'indexing_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'indexing' ),
              
               'annotation_dbpedia': os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'annotation', 'dbpedia' ),
               'annotation_wikidata':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'annotation', 'wikidata' ),
               'annotation_geonames':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'annotation', 'geonames' ),
              
               }
    
    USER_AGENT = 'ISSA extraction script' 
    
    DEBUG=True    

class cfg_download_agritrop_metadata(cfg_pipeline):
    LANGUAGE = {'fr': 'fre',
                'en': 'eng',
                'es': 'spa',
                'pt': 'por'} [_LANG]
    
    #OAI_DATASET_NAME = f'issa_{LANGUAGE}' 
    OAI_DATASET_NAME = 'driver' 
    
    OAI_ENDPOINT_START = 'https://agritrop.cirad.fr/cgi/oai2?verb=ListRecords&metadataPrefix=oai_dc&set=%s'
    OAI_ENDPOINT_CONTINUE ='https://agritrop.cirad.fr/cgi/oai2?verb=ListRecords&resumptionToken=%s'
    #OAI_DELTA_RESUMPTION_TOKEN = 'metadataPrefix=oai_dc&offset=%s&set=%s'
    USER_AGENT = 'ISSA extraction script' 
    
    OAI_NS = {'oai': 'http://www.openarchives.org/OAI/2.0/', 
              'dc' : 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/'}

    
    #RAW_DATA_FILENAME = f'{_METADATA_PREFIX}_{_LANG}.raw.tsv'
    RAW_DATA_FILENAME = f'{_METADATA_PREFIX}.raw.tsv'
    OUTPUT_PATH = './output'
    #LOG_PATH = '../logs'

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
                        'title_lang': None,
                        'title_lang_score': None,
                        'abstract_lang': None,
                        'abstract_lang_score': None,
                        'proc_date': None
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
    #DEBUG = True


class cfg_process_agritrop_metadata(cfg_pipeline):
    #LANGUAGE = _LANG
    #TDOO: refactor for generality
    LANG_MAP = {'fre': 'fr',
                'eng': 'en',
                'spa': 'es',
                'por': 'pt',
                'ger': 'de',
                'ara': 'ar',
                'dut': 'nl',
                'ind': 'id',
                'lao': 'lo',
                'mlg': 'mg',
                'tha': 'th',
                'vie': 'vi'}

    RAW_DATA_FILENAME = cfg_download_agritrop_metadata.RAW_DATA_FILENAME # f'{_METADATA_PREFIX}_{_LANG}.raw.tsv'
    #PROCESSED_DATA_FILENAME = f'{_METADATA_PREFIX}_{_LANG}.tsv'
    PROCESSED_DATA_FILENAME = f'{_METADATA_PREFIX}.tsv'

    
    INPUT_PATH = cfg_download_agritrop_metadata.OUTPUT_PATH
    OUTPUT_PATH = INPUT_PATH
    #LOG_PATH = '../logs'
    
    AGROVOC_SPARQL_WRAPPER = SPARQL_Endpoint_Wrapper('http://riolan.cirad.fr/sparql')
        
    ARGROVOC_QUERY_TEMPLATE = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
    PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
    SELECT ?concept ?label 
    WHERE { 
      VALUES(?concept) {%s}
      
      ?concept a skos:Concept . 
      ?concept skosxl:prefLabel/skosxl:literalForm ?label.
      
      FILTER(langMatches(lang(?label), '%s')) 
    }  
    '''
    
    DETECT_LANG = False
    BEST_EFFORT_LANG_DETECTION = False
    FILL_NOT_DETECTED_LANG = True

class cfg_create_dataset_repository(cfg_pipeline):
    #LANGUAGE = _LANG
    
    PROCESSED_DATA_FILENAME = cfg_process_agritrop_metadata.PROCESSED_DATA_FILENAME
 
    INPUT_PATH = cfg_process_agritrop_metadata.OUTPUT_PATH
    #LOG_PATH = '../logs'
    #OUTPUT_ROOT_PATH =  _ISSA_DATA_ROOT
    DATASET_NAME = _ISSA_DATASET
    # DATASET_ROOT_PATH = os.path.join(_ISSA_DATA_ROOT, _ISSA_DATASET)
    
    # CURRENT_DATE = datetime.datetime.now().strftime('%Y%m%d')
    # LATEST_UPDATE = [x for x in (sorted(os.listdir(DATASET_ROOT_PATH), reverse=True) ) if os.path.isdir(x)]
    # LATEST_UPDATE = LATEST_UPDATE[0] if LATEST_UPDATE else CURRENT_DATE

    # FILES_LOC = {'metadata' :        os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE),
    #              'tsv' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'labels' ),
    #              'txt' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'txt' ),
    #              'url' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'pdf' ),
    #              'pdf' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'pdf' ),
    #              'metadata_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'json', 'metadata' ),
    #              'fulltext_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'json', 'fulltext' ),
    #              'coalesced_json' :  os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'json', 'coalesced' ),
    #              'xml' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'xml' ),
    #              'indexing_text' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'indexing' ),
    #              'indexing_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'indexing' ),
                 
    #              'annotation_spotlight': os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'annotation', 'dbpedia-spotlight' ),
    #              'annotation_ef':        os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, 'annotation', 'entity-fishing' ),
                 
    #              }

    REMOVE_FILES = False
    SAVE_LABELS_TSV = True
    SAVE_PDF_URL = True
    SAVE_META_TEXT = True
    SAVE_META_JSON = True
    
    OUTPUT_SUFFIX = '.meta'
    
    JSON_SCHEMA={'paper_id' : '',
                   'metadata' : {'title': '',
                               'authors': '',
                               'title_lang': {'code': '', 'score': 0.0},
                               'abstract_lang': {'code': '', 'score': 0.0},
                               },
                   'abstract' : [{'text' : ''}],
                 }
    
    METADATA_TO_JSON_MAP = {'agritrop_id' : ['paper_id'],
                             'title'       : ['metadata', 'title'],
                             'abstract'    : ['abstract', 0, 'text'],
                             'authors'              : ['metadata', 'authors'],
                             'title_lang'           : ['metadata', 'title_lang','code'] ,
                             'title_lang_score'     : ['metadata', 'title_lang','score'] ,
                             'abstract_lang'        : ['metadata', 'abstract_lang','code'] ,
                             'abstract_lang_score'  : ['metadata', 'abstract_lang','score'] ,
                
                            }

class cfg_extract_text_from_pdf(cfg_pipeline):
    # Dependency on the create_dataset-repository config
    #FILES_LOC = cfg_create_dataset_repository.FILES_LOC
    FILES_LOC = cfg_pipeline.FILES_LOC
    
    INPUT_PATH = FILES_LOC['pdf']
    INPUT_PATTERN = '*.url'
    
    OUTPUT_PATH = FILES_LOC['fulltext_json']
    OUTPUT_SUFFIX = '.grobid'
    OVERWRITE_EXISTING = False
    OUTPUT_IF_BAD_PDF = True
    
    CACHE_PDF = True
    CACHE_PATH= _PDF_CACHE
    CACHE_UNREADABLE_PATH = _PDF_CACHE_UNREADABLE
    
    #DATASET_ROOT_PATH = os.path.join(_ISSA_DATA_ROOT, _ISSA_DATASET)
        
    SAVE_XML = True
    SAVE_TEXT= True  
    OUTPUT_XML_PATH = FILES_LOC['xml']
    OUTPUT_TXT_PATH = FILES_LOC['txt']  
    OUTPUT_PDF_PATH = FILES_LOC['pdf']
    
    DOWNLOAD_DELAY = 5 #sec

    GROBID_URL = 'http://localhost:8070'
    GROBID_API_URL = f'{GROBID_URL}/api/processFulltextDocument'
    
    #OUTPUT_ROOT_PATH = _ISSA_DATA_ROOT
    #DATASET_NAME = _ISSA_DATASET
    #LOG_PATH = '../logs'
    
    TEI_BASE_URL = "http://www.tei-c.org/ns/1.0/"
    TEI_NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    OUTPUT_SCHEMA={'paper_id' : '',
                     'metadata' : {'title': '',
                                   'authors': '',
                                   'keywords': '',
                                   'title_lang': {'code': '', 'score': 0.0},
                                   'abstract_lang': {'code': '', 'score': 0.0},
                                   'body_lang': {'code': '', 'score': 0.0} },
                     'abstract' : [{'text' : ''}],
                     'body_text': [{'text' : ''},],
                     #'ref_entries': ''
                     }
    
    XML_DICT_MAP = {'title':    ('//tei:titleStmt/tei:title//text()', ['metadata', 'title']),
                   'abstract':  ('//tei:profileDesc/tei:abstract//text()' ,  ['abstract' , 0, 'text']),
                   'body_text': ('//tei:body//tei:p[text()]', ['body_text']), # #return root.xpath("//tei:body//tei:p//text()", namespaces=NS) #- more
                   #'authors':   ('//tei:fileDesc//tei:author', ['metadata', 'authors']),
                   'keywords':  ('//tei:profileDesc/tei:textClass/tei:keywords/tei:term/text()' , ['metadata', 'keywords']), }
                   #'bib_entries': ('//tei:text//tei:listBibl/tei:biblStruct', ['bib_entries'])}
    
    MERGE_BODY_TEXT = True
    MERGE_SEPARATOR = os.linesep
    
    #DEFAULT_LANGUAGE = _LANG
    DETECT_LANG = False
    BEST_EFFORT_LANG_DETECTION = False
    
    #INCLUDE_AUTHORS = False
    #INCLUDE_BIB = False
    
    #DEBUG=True
    

class cfg_coalesce_meta_json(cfg_pipeline):
   
    DO_COALESE = True
    #LOG_PATH = '../logs'
    
    INPUT_PATTERN = '*.json'
    OUTPUT_SUFFIX = ''
  
    FILES_LOC = cfg_pipeline.FILES_LOC
    INPUT_METADATA_PATH = FILES_LOC['metadata_json']
    INPUT_FULLTEXT_PATH = FILES_LOC['fulltext_json']
    OUTPUT_PATH = FILES_LOC['coalesced_json']
   
    
class cfg_indexing_preprocess(cfg_pipeline):
    INPUT_PATTERN = '*.json'
    OUTPUT_SUFFIX = '.txt'
    
    PARTS_SEPARATOR = os.linesep + os.linesep

    FILES_LOC = cfg_pipeline.FILES_LOC    

    INPUT_PATH = FILES_LOC['coalesced_json']
    OUTPUT_PATH = FILES_LOC['indexing_text']
    OUTPUT_LANG = ['en', 'fr']
   
    # json path to                 text                      language      
    JSON_TEXT_MAP= { 'title':    (['metadata', 'title'],     ['metadata', 'title_lang', 'code']),
                    'abstract':  (['abstract', 0, 'text'],   ['metadata', 'abstract_lang', 'code']),
                    'keywords':  (['metadata', 'keywords'],  ['metadata', 'body_lang', 'code']),
                    'body_text': (['body_text' , 0, 'text'], ['metadata', 'body_lang', 'code']) 
        
                   }
    # order in which determine a document language
    LANGUAGE_DETERMINATORS = ['body_text', 'abstract', 'title']
 
class cfg_indexing_postprocess(cfg_pipeline): 
    FILES_LOC = cfg_pipeline.FILES_LOC  
    
    INPUT_PATTERN= '**/*%s*' % _ANNIF_SUFFIX
    INPUT_TSV_PATH = FILES_LOC['indexing_text']    
    
    OUTPUT_SUFFIX = '%s.json' % _ANNIF_SUFFIX
    OUTPUT_JSON_PATH = FILES_LOC['indexing_json']
    
    OUTPUT_SCHEMA={'paper_id' : '',
                   'model': '',
                   'language': '',
                   'subjects' : [{'uri': '',
                                  'label': '',
                                   'conf_score': 0.0,
                                   'rank': 0}]
                   }

# This config may go somewhere else because this step is not a part of the 
# pipeline. Try to keep it independent    
class cfg_indexing_training(object):
    
    LOG_PATH = '../logs' 
    
    INPUT_PATH=os.path.join(_ISSA_DATA_ROOT, _ISSA_DATASET)
    INPUT_PATTERN = '**/coalesced/*.json'
    LABEL_PATTERN='**/labels/'
    
    OUTPUT_SUFFIX = '.txt'
    
    PARTS_SEPARATOR = os.linesep + os.linesep
    
    
    OUTPUT_PATH = os.path.join(_ISSA_DATA_ROOT, 'training')
    
    TRAINING_FILES_LOC = {'en' : { 'train' : os.path.join(OUTPUT_PATH, 'en', 'train'),
                                   'test'  : os.path.join(OUTPUT_PATH, 'en', 'test') },
                          'fr' : { 'train' : os.path.join(OUTPUT_PATH, 'fr', 'train'),
                                   'test'  : os.path.join(OUTPUT_PATH, 'fr', 'test') }
                          }

    # json path to                 text                      language      
    JSON_TEXT_MAP= { 'title':    (['metadata', 'title'],     ['metadata', 'title_lang', 'code']),
                    'abstract':  (['abstract', 0, 'text'],   ['metadata', 'abstract_lang', 'code']),
                    'keywords':  (['metadata', 'keywords'],  ['metadata', 'body_lang', 'code']),
                    'body_text': (['body_text' , 0, 'text'], ['metadata', 'body_lang', 'code']) 
        
                   }
    # order in which to determine a document language
    LANGUAGE_DETERMINATORS = ['body_text', 'abstract', 'title']
    
    MIN_TEXT_LENGTH = 0
    PARTS_SEPARATOR = os.linesep + os.linesep
    TEST_SET_SIZE = 0.2

class cfg_annotation_dbpedia(cfg_pipeline): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    INPUT_PATH = FILES_LOC['coalesced_json']
    OUTPUT_PATH = FILES_LOC['annotation_dbpedia']
    
    INPUT_PATTERN = '*.json'
    OUTPUT_SUFFIX = '.json'

    OUTPUT_OVERWRITE_EXISTING = False
    
    SPOTLIGHT_ENDPOINTS = {
        #'en': 'http://localhost:2222/rest/annotate',
        #'fr': 'http://localhost:2223/rest/annotate',
        'en': 'https://api.dbpedia-spotlight.org/en/annotate',
        'fr': 'https://api.dbpedia-spotlight.org/fr/annotate',

    }
    
    SPOTLIGHT_CONFIDENCE= 0.50
    SPOTLIGHT_SUPPORT   = 10
    
        # json path to                 text                      language      
    JSON_TEXT_MAP= { 'title':    (['metadata', 'title'],     ['metadata', 'title_lang', 'code']),
                    'abstract':  (['abstract', 0, 'text'],   ['metadata', 'abstract_lang', 'code']),
                    'body_text': (['body_text' , 0, 'text'], ['metadata', 'body_lang', 'code']) 
                   }
    
    REMOVE_HEADER = True
    REMOVE_TEXT = True
    
    ASYNCH_PROCESSING = True
    ASYNCH_MAX_WORKERS = 10

class cfg_annotation_wikidata(cfg_pipeline): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    INPUT_PATH = FILES_LOC['coalesced_json']
    OUTPUT_PATH = FILES_LOC['annotation_wikidata']
    
    INPUT_PATTERN = '*.json'
    OUTPUT_SUFFIX = '.json'    
    
    OUTPUT_OVERWRITE_EXISTING = True
        
        # json path to                 text                      language      
    JSON_TEXT_MAP= { 'title':    (['metadata', 'title'],     ['metadata', 'title_lang', 'code']),
                    'abstract':  (['abstract', 0, 'text'],   ['metadata', 'abstract_lang', 'code']),
                    'body_text': (['body_text' , 0, 'text'], ['metadata', 'body_lang', 'code']) 
                   }
    
        
    #ENTITY_FISHING_ENDPOINT = 'http://localhost:8090/service/disambiguate'
    ENTITY_FISHING_ENDPOINT = 'https://cloud.science-miner.com/nerd//service/disambiguate'
    
    REMOVE_HEADER = False
    REMOVE_TEXT = True
    REMOVE_GLOBAL_CATEGORIES = False
    
    ASYNCH_PROCESSING = True
    ASYNCH_MAX_WORKERS = 10
   
class cfg_annotation_geonames(cfg_pipeline): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    INPUT_PATH = FILES_LOC['annotation_wikidata']
    OUTPUT_PATH = FILES_LOC['annotation_geonames']
    
    INPUT_PATTERN = '*.json'
    OUTPUT_SUFFIX = '.json'    
    
    OUTPUT_OVERWRITE_EXISTING = True
        
        # json path to                 text                      language                 default lang
    JSON_TEXT_MAP= { 'title':    (['title', 'text'],      ['title', 'language', 'lang'] , 'fr'  ),
                    'abstract':  (['abstract', 'text'],   ['abstract', 'language', 'lang'], 'fr' ),
                    'body_text': (['body_text' ,'text'],  ['body_text', 'language', 'lang'], 'fr' ) 
                   }
    
    
    ENTITY_FISHING_ENDPOINTS = {
        #'disambiguation' : 'http://localhost:8090/service/disambiguate',
        #'concept_lookup': 'http://localhost:8090/servic/service/kb/concept/',
        'disambiguation' : 'https://cloud.science-miner.com/nerd//service/disambiguate/',
        'concept_lookup': 'https://cloud.science-miner.com/nerd//service/kb/concept/',}

    ASYNCH_PROCESSING = True
    ASYNCH_MAX_WORKERS = 10
 
   