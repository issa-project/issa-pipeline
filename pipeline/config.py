# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 19:14:38 2021

@author: abobashe
"""

import os
import datetime
from  util import SPARQL_Endpoint_Wrapper

# read environment variables defined and exported in env.sh
# if an environment variable is not specified default is assigned

def read_env_var(var_name):
    return os.environ[var_name] if var_name in os.environ else None


_ISSA_DATA_ROOT	= read_env_var('ISSA_DATA_ROOT') 			or '~/ISSA/data'
_ISSA_DATASET    	= read_env_var('ISSA_DATASET') 				or 'dataset-1-0'

_METADATA_PREFIX 	= read_env_var('METADATA_PREFIX') 			or 'corpus'  
_ANNIF_SUFFIX    	= read_env_var('ANNIF_SUFFIX') 				or 'annif'

_PDF_CACHE       	= read_env_var('PDF_CACHE') 				or '~/ISSA/data/pdf_cache'
_PDF_CACHE_UNREADABLE = read_env_var('PDF_CACHE_UNREADABLE') 	or '~/ISSA/data/pdf_cache/unreadable'

# Directories of data files relative to LATEST_UPDATE_DIR

_REL_META 		= read_env_var('REL_META') 					or '.'
_REL_META_JSON 	= read_env_var('REL_META_JSON') 			or 'json/metadata'
_REL_PDF  		= read_env_var('REL_PDF') 					or 'pdf'

_REL_GROBID_XML  	= read_env_var('REL_GROBID_XML') 			or 'xml'
_REL_GROBID_JSON  	= read_env_var('REL_GROBID_JSON') 			or 'json/fulltext'
_REL_COAL_JSON  	= read_env_var('REL_COAL_JSON') 			or 'json/coalesced'

_REL_ANNIF_LABELS 	= read_env_var('REL_ANNIF_LABELS') 			or 'labels'
_REL_ANNIF_TEXT   	= read_env_var('REL_ANNIF_TEXT') 			or 'txt'
_REL_ANNIF		= read_env_var('REL_ANNIF') 			   	or 'indexing'

_REL_ANNIF		= read_env_var('REL_ANNIF') 			    	or 'indexing'

_REL_SPOTLIGHT	= read_env_var('REL_SPOTLIGHT') 		   	or 'annotation/dbpedia'
_REL_EF			= read_env_var('REL_EF')		 		    	or 'annotation/wikidata'
_REL_GEONAMES		= read_env_var('REL_GEONAMES') 		     	or 'annotation/geonames'
_REL_PYCLINREC	= read_env_var('REL_PYCLINREC') 		     or 'annotation/agrovoc'

_REL_RDF			= read_env_var('REL_RDF') 		     		or 'rdf'


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

    FILES_LOC = {'metadata' :      os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_META ),
               'tsv' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_ANNIF_LABELS ),
               'txt' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_ANNIF_TEXT ),
               'url' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_PDF ),
               'pdf' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_PDF ),
               'metadata_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_META_JSON ),
               'fulltext_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_GROBID_JSON  ),
               'coalesced_json' :  os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_COAL_JSON  ),
               'xml' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_GROBID_XML ),
               'indexing_text' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_ANNIF ),
               'indexing_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_ANNIF ),
              
               'annotation_dbpedia': os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_SPOTLIGHT ),
               'annotation_wikidata':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_EF ),
               'annotation_geonames':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_GEONAMES ),
               
               'annotation_agrovoc':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_PYCLINREC ),             
               }

    
    USER_AGENT = 'ISSA extraction script' 
    
    DEBUG=False    

class cfg_download_corpus_metadata(cfg_pipeline):

    OAI_DATASET_NAME = 'driver' 
    
    OAI_ENDPOINT_START = 'https://agritrop.cirad.fr/cgi/oai2?verb=ListRecords&metadataPrefix=oai_dc&set=%s'
    OAI_ENDPOINT_CONTINUE ='https://agritrop.cirad.fr/cgi/oai2?verb=ListRecords&resumptionToken=%s'
    #OAI_DELTA_RESUMPTION_TOKEN = 'metadataPrefix=oai_dc&offset=%s&set=%s'
    USER_AGENT = 'ISSA extraction script' 
    
    OAI_NS = {'oai': 'http://www.openarchives.org/OAI/2.0/', 
              'dc' : 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/'}

    
    RAW_DATA_FILENAME = f'{_METADATA_PREFIX}.raw.tsv'
    OUTPUT_PATH = './output'

    SINGLE_FIELD_MAP = {'paper_id' : 'oai:header/oai:identifier',
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
                       'descriptors_uris' :'' ,
                       'descriptors_labels': '',
                       'identifiers' : 'oai:metadata/oai_dc:dc/dc:identifier',
                       'licenses' : 'oai:metadata/oai_dc:dc/dc:rights',
                       'relations' : 'oai:metadata/oai_dc:dc/dc:relation', #ideally it should have XML path expression [starts-with(.,"http")] butit is not supported
                       'same_as' : '',
                       'identifiers' : 'oai:metadata/oai_dc:dc/dc:identifier',
                       'types' : 'oai:metadata/oai_dc:dc/dc:type',
                      }
    #DEBUG = True


class cfg_process_corpus_metadata(cfg_pipeline):
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
                'vie': 'vi',
                'default': 'en'}

    RAW_DATA_FILENAME = cfg_download_corpus_metadata.RAW_DATA_FILENAME 
    PROCESSED_DATA_FILENAME = f'{_METADATA_PREFIX}.tsv'
    
    INPUT_PATH = cfg_download_corpus_metadata.OUTPUT_PATH
    OUTPUT_PATH = INPUT_PATH
    
    VOCAB_SPARQL_WRAPPER = SPARQL_Endpoint_Wrapper('http://riolan.cirad.fr/sparql')
        
    VOCAB_QUERY_TEMPLATE = '''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
    PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#> 
    SELECT ?uri ?label 
    WHERE { 
      VALUES(?uri) {%s}
      
      ?uri a skos:Concept . 
      OPTIONAL{?uri skosxl:prefLabel/skosxl:literalForm ?langlabel
  				FILTER(langMatches(lang(?langlabel), '%s'))
  	  }
      OPTIONAL{?uri skosxl:prefLabel/skosxl:literalForm ?defaultlabel.
 	           FILTER(langMatches(lang(?defaultlabel), 'en') )
  	  }
      OPTIONAL{?uri skosxl:prefLabel/skosxl:literalForm ?nolanglabel.
 	           FILTER(langMatches(lang(?nolanglabel), '') )
  	  } 
      
      BIND(COALESCE(?langlabel, ?defaultlabel, ?nolanglabel) AS ?label)
    }  
    '''
    
    DETECT_LANG = True
    BEST_EFFORT_LANG_DETECTION = False
    FILL_NOT_DETECTED_LANG = True

class cfg_create_dataset_repository(cfg_pipeline):
    
    INPUT_PATH = cfg_process_corpus_metadata.OUTPUT_PATH
    INPUT_METADATA_FILENAME = cfg_process_corpus_metadata.PROCESSED_DATA_FILENAME
    RAW_METADATA_FILENAME = cfg_process_corpus_metadata.RAW_DATA_FILENAME

    DATASET_NAME = _ISSA_DATASET

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
    
    METADATA_TO_JSON_MAP = {'paper_id' : ['paper_id'],
                             'title'       : ['metadata', 'title'],
                             'abstract'    : ['abstract', 0, 'text'],
                             'authors'              : ['metadata', 'authors'],
                             'title_lang'           : ['metadata', 'title_lang','code'] ,
                             'title_lang_score'     : ['metadata', 'title_lang','score'] ,
                             'abstract_lang'        : ['metadata', 'abstract_lang','code'] ,
                             'abstract_lang_score'  : ['metadata', 'abstract_lang','score'] ,
                            }

class cfg_extract_text_from_pdf(cfg_pipeline):

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
    
    SAVE_XML = False
    SAVE_TEXT= False  
    OUTPUT_XML_PATH = FILES_LOC['xml']
    OUTPUT_TXT_PATH = FILES_LOC['txt']  
    OUTPUT_PDF_PATH = FILES_LOC['pdf']
    
    DOWNLOAD_DELAY = 5 #sec

    GROBID_URL = 'http://localhost:8070'
    GROBID_API_URL = f'{GROBID_URL}/api/processFulltextDocument'
    
    
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
    
    DETECT_LANG = True
    BEST_EFFORT_LANG_DETECTION = False
    
    #INCLUDE_AUTHORS = False
    #INCLUDE_BIB = False

class cfg_coalesce_meta_json(cfg_pipeline):
   
    FILES_LOC = cfg_pipeline.FILES_LOC
    
    INPUT_PATTERN = '*.json'
    OUTPUT_SUFFIX = ''

    INPUT_METADATA_PATH = FILES_LOC['metadata_json']
    INPUT_FULLTEXT_PATH = FILES_LOC['fulltext_json']
    OUTPUT_PATH = FILES_LOC['coalesced_json']
   
    DO_COALESE = True
    
class cfg_indexing_preprocess(cfg_pipeline):
        
    FILES_LOC = cfg_pipeline.FILES_LOC
   
    INPUT_PATTERN = '*.json'
    OUTPUT_SUFFIX = '.txt'
    
    PARTS_SEPARATOR = os.linesep + os.linesep

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
 
    #METADATA_FILE = os.path.join(INPUT_PATH,
    #                             sorted(os.listdir(INPUT_PATH), reverse=True) [0], #LATEST_UPDATE,
    #                             f'{_METADATA_PREFIX}.tsv')
    
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


# Commonn config setting for the annoattion scripts
class cfg_annotation(cfg_pipeline): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    INPUT_PATH = FILES_LOC['coalesced_json']
    INPUT_PATTERN = '*.json'

    OUTPUT_PATH = '' # has to be overwritten
    OUTPUT_SUFFIX = '.json'
    OUTPUT_OVERWRITE_EXISTING = False

    # json path to                 text                      language      
    JSON_TEXT_MAP= { 'title':    (['metadata', 'title'],     ['metadata', 'title_lang', 'code']),
                    'abstract':  (['abstract', 0, 'text'],   ['metadata', 'abstract_lang', 'code']),
                    'body_text': (['body_text' , 0, 'text'], ['metadata', 'body_lang', 'code']) 
                   }
    
    REMOVE_HEADER = True
    REMOVE_TEXT = True

    ASYNCH_PROCESSING = True
    ASYNCH_MAX_WORKERS = 10


class cfg_annotation_dbpedia(cfg_annotation): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    OUTPUT_PATH = FILES_LOC['annotation_dbpedia']
   
    SPOTLIGHT_ENDPOINTS = {
        'en': 'http://localhost:2222/rest/annotate',
        'fr': 'http://localhost:2223/rest/annotate',
        #'en': 'https://api.dbpedia-spotlight.org/en/annotate',
        #'fr': 'https://api.dbpedia-spotlight.org/fr/annotate',

    }
    
    SPOTLIGHT_CONFIDENCE= 0.50
    SPOTLIGHT_SUPPORT   = 10
    
class cfg_annotation_wikidata(cfg_annotation): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    OUTPUT_PATH = FILES_LOC['annotation_wikidata']

    ENTITY_FISHING_ENDPOINT = 'http://localhost:8090/service/disambiguate'
    #ENTITY_FISHING_ENDPOINT = 'https://cloud.science-miner.com/nerd/service/disambiguate'
    
    REMOVE_GLOBAL_CATEGORIES = False
    
   
class cfg_annotation_geonames(cfg_annotation): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    INPUT_PATH = FILES_LOC['annotation_wikidata']
    OUTPUT_PATH = FILES_LOC['annotation_geonames']

    # json path to                 text                      language                 default lang
    JSON_TEXT_MAP= { 'title':    (['title', 'text'],      ['title', 'language', 'lang'] , 'fr'  ),
                    'abstract':  (['abstract', 'text'],   ['abstract', 'language', 'lang'], 'fr' ),
                    'body_text': (['body_text' ,'text'],  ['body_text', 'language', 'lang'], 'fr' ) 
                   }
  
    
    ENTITY_FISHING_ENDPOINTS = {
        'disambiguation' : 'http://localhost:8090/service/disambiguate',
        'concept_lookup': 'http://localhost:8090/service/kb/concept'}
        #'disambiguation' : 'https://cloud.science-miner.com/nerd//service/disambiguate/',
        #'concept_lookup': 'https://cloud.science-miner.com/nerd//service/kb/concept/',}
    

class cfg_annotation_agrovoc(cfg_annotation): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    OUTPUT_PATH = FILES_LOC['annotation_agrovoc']
    
    PYCLINREC_ENDPOINT = 'http://localhost:5000/annotate'
    
    PYCLINREC_CONFIDENCE= 0.15
    
