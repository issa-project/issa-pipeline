# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 19:14:38 2021

@author: abobashe

This module contains configuration settings for the ISSA pipeline Python scripts.
Each class defines a set of settings for a specific module of the pipeline.
"""

import os
import datetime
import numpy as np
from util import SPARQL_Endpoint_Wrapper, read_env_var

#%%
# Read environment variables defined in env.sh
# if an environment variable is not specified default is assigned
#                                        var name               default value                                                
_ISSA_DATA_ROOT	        = read_env_var('ISSA_DATA_ROOT' ,       os.path.expanduser('~/ISSA-2/data/hal') )
_ISSA_DATASET    	    = read_env_var('ISSA_DATASET' ,         'dataset-2-0')
_ISSA_LOG               = read_env_var('ISSA_PIPELINE_LOG',     '../logs')

_METADATA_PREFIX 	    = read_env_var('METADATA_PREFIX',       'hal_meta_test' )
_ANNIF_SUFFIX    	    = read_env_var('ANNIF_SUFFIX',          'annif')

_PDF_CACHE       	    = read_env_var('PDF_CACHE',             os.path.expanduser('~/ISSA-2/data/hal/pdf_cache') )
_PDF_CACHE_UNREADABLE   = read_env_var('PDF_CACHE_UNREADABLE',  os.path.expanduser('~/ISSA-2/data/hal/pdf_cache/unreadable'))

# Directories of data files relative to the LATEST_UPDATE_DIR

_REL_META 		        = read_env_var('REL_META',              '.' )
_REL_META_JSON 	        = read_env_var('REL_META_JSON',         'json/metadata')
_REL_PDF  		        = read_env_var('REL_PDF',               'pdf')

_REL_GROBID_XML  	    = read_env_var('REL_GROBID_XML',        'xml' )
_REL_GROBID_TXT  	    = read_env_var('REL_GROBID_TXT',        'txt' )
_REL_GROBID_JSON  	    = read_env_var('REL_GROBID_JSON',       'json/fulltext')
_REL_COAL_JSON  	    = read_env_var('REL_COAL_JSON',         'json/coalesced')
_REL_OPENALEX 	        = read_env_var('REL_OPENALEX',          'openalex')

_REL_SPOTLIGHT	        = read_env_var('REL_SPOTLIGHT',         'annotation/dbpedia')
_REL_EF			        = read_env_var('REL_EF',                'annotation/wikidata')
_REL_GEONAMES		    = read_env_var('REL_GEONAMES',          'annotation/geonames')
_REL_PYCLINREC	        = read_env_var('REL_PYCLINREC',         'annotation/mesh')

_REL_RDF			    = read_env_var('REL_RDF',                'rdf')


class cfg_pipeline(object):
    """
    Shared settings
    """

    LOG_PATH = _ISSA_LOG 
   
    DATASET_ROOT_PATH = os.path.join(_ISSA_DATA_ROOT, _ISSA_DATASET)
   
    CURRENT_DATE = datetime.datetime.now().strftime('%Y%m%d')
    LATEST_UPDATE = [x for x in (sorted(os.listdir(DATASET_ROOT_PATH), reverse=True) ) ]
                         #    if os.path.isdir( os.path.join(DATASET_ROOT_PATH, x) )] # TODO: check weird behavior

    LATEST_UPDATE = LATEST_UPDATE[0] if LATEST_UPDATE else CURRENT_DATE

    FILES_LOC = {
               'metadata' :        os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_META ),
               'url' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_PDF ),
               'pdf' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_PDF ),
               'metadata_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_META_JSON ),
               'fulltext_json' :   os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_GROBID_JSON  ),
               'coalesced_json' :  os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_COAL_JSON  ),
               'xml' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_GROBID_XML ),
               'txt' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_GROBID_TXT ),
               'openalex' :        os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_OPENALEX ),
               'rdf' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_RDF ),
              
               'annotation_dbpedia': os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_SPOTLIGHT ),
               'annotation_wikidata':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_EF ),
               'annotation_geonames':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_GEONAMES ),
               'annotation_pyclinrec':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_PYCLINREC ),            
               }

    
    USER_AGENT = 'ISSA extraction script' 
    
    # TSV metadata file where to look for new documents
    DOCUMENT_URI_TEMPLATE = 'http://data-issa.cirad.fr/document/%s'
    
    DEBUG=True


class cfg_download_corpus_metadata(cfg_pipeline):

    OAI_DATASET_NAME = 'collection:EUROMOV-DHM' 
    
    OAI_ENDPOINT_START = 'https://api.archives-ouvertes.fr/oai/hal/?verb=ListRecords&metadataPrefix=oai_dc&set=%s'
    OAI_ENDPOINT_CONTINUE ='https://api.archives-ouvertes.fr/oai/hal/?verb=ListRecords&resumptionToken=%s'

    USER_AGENT = 'ISSA extraction script' 
    
    OAI_NS = {'oai': 'http://www.openarchives.org/OAI/2.0/', 
              'dc' : 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
              'xml': 'http://www.w3.org/XML/1998/namespace'}

    
    RAW_DATA_FILENAME = f'{_METADATA_PREFIX}.raw.tsv'
    OUTPUT_PATH = './output'

    SINGLE_FIELD_MAP = {'paper_id' : 'oai:header/oai:identifier',
                        'datestamp' :  'oai:header/oai:datestamp',

                        'language' : 'oai:metadata/oai_dc:dc/dc:language',
                        'year' : 'oai:metadata/oai_dc:dc/dc:date',
                        }

    MULTI_FIELD_MAP = { 'sources': 'oai:metadata/oai_dc:dc/dc:source',
                        'relations': 'oai:metadata/oai_dc:dc/dc:relation',
                        'types': 'oai:metadata/oai_dc:dc/dc:type',
                        'rights': 'oai:metadata/oai_dc:dc/dc:rights',
                        'identifiers': 'oai:metadata/oai_dc:dc/dc:identifier',
                    
                        'authors': 'oai:metadata/oai_dc:dc/dc:creator',
                        'contributors': 'oai:metadata/oai_dc:dc/dc:contributor',
                        'publishers': 'oai:metadata/oai_dc:dc/dc:publisher',
                        'coverage': 'oai:metadata/oai_dc:dc/dc:coverage',

                        'titles_lang' : [],
                        'titles' : 'oai:metadata/oai_dc:dc/dc:title/[@xml:lang]',

                        'descriptions': 'oai:metadata/oai_dc:dc/dc:description',
                        'abstracts_lang': [],
                        'abstracts': 'oai:metadata/oai_dc:dc/dc:description/[@xml:lang]',

                        'subjects': 'oai:metadata/oai_dc:dc/dc:subject',
                        'keywords_lang': [],
                        'keywords': 'oai:metadata/oai_dc:dc/dc:subject/[@xml:lang]',

                    }

    DEBUG = False


class cfg_process_corpus_metadata(cfg_pipeline):

    RAW_DATA_FILENAME = cfg_download_corpus_metadata.RAW_DATA_FILENAME 
    PROCESSED_DATA_FILENAME = f'{_METADATA_PREFIX}.tsv'
    
    INPUT_PATH = cfg_download_corpus_metadata.OUTPUT_PATH
    OUTPUT_PATH = INPUT_PATH

    DETECT_LANG = True
    LANG_DETECTION_METHOD = 'langdetect' # 'cld2' | 'langdetect', 
    BEST_EFFORT_LANG_DETECTION = False
    FILL_NOT_DETECTED_LANG = True
  
    PAPER_ID_REGEX = r'[^:]+$'
    YEAR_REGEX = r'\b\d{4}\b'

    DOI_REGEX = r'\b10\.\d{4,9}/[-.;()/:\w]+'
    URI_REGEX = r'\w+:(\/?\/?)[^\s]+'
    URL_REGEX = r'^https?:(\/?\/?)[^\s]+'

    DESCRIPTOR_URI_REGEX = r'^http:(\/?\/?)[^\s]+'

    DOMAIN_CODE_REGEX = r'^[A-Z]\d{2}\b'
    DOMAIN_NAMESPACE = 'https://data.archives-ouvertes.fr/subject/' 

    LANG_MAP = {'fr': 'fre',
            'en': 'eng',
            'es': 'spa',
            'pt': 'por',
            'de': 'ger',
            'ar': 'ara',
            'nl': 'dut',
            'id': 'ind',
            'lo': 'lao',
            'mg': 'mlg',
            'th': 'tha',
            'vi': 'vie',
            'default': 'eng'}

    BEFORE_COMMA_REGEX = r'[^\r\n,]+'
    TIDY_TEXT_REGEX = r'^\s+|\t|\n|\r|\s+$'
    DOUBLE_QUOTES_REGEX = r'"' #  r'"{2,}'
    #TABS_AND_QUOTES_REGEX = r'[\n\r\t\"]+'
    #MULTIPLE_WHITESPACES_REGEX = r'\s+'
    #AUDIENCE_REGEX = r'International audience|National audience'
    NON_SOURCES_REGEX = r'^EISSN:|^ISSN:|^http|^[0-9]+$' # use with remove # this might not be nessesary
    SOURCES_REFEX = r'^(?!EISSN:|ISSN:|http:|https:|[0-9]+).*$' #use with filter 
    ACCESS_REGEX = r'^info:eu-repo/semantics.+'
    LICENSE_URI_REGEX = r'^http:.+licenses.+'
    HAL_URL_REGEX = r'^https?:\S*-\d+$'
    PDF_URI_REGEX = r'^https?:.+\.pdf$'
    DOMAINS_SUBJECTS_REGEX= r'\[(.*?)\]'
    MESH_REGEX = r'^MESH:\s' #r'^MESH:\s(.+)$'

    MESH_SPARQL_WRAPPER = SPARQL_Endpoint_Wrapper('http://localhost:8891/sparql') 
                                                  #'https://id.nlm.nih.gov/mesh/sparql'

    # NOTE: The mapping query have to follow a rule: the first returned variable 
    # is a lookup key, the second is a lookup value 
    MESH_QUERY_TEMPLATE = '''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
    PREFIX mesh: <http://id.nlm.nih.gov/mesh/>

    SELECT ?label ?uri
    FROM <http://id.nlm.nih.gov/mesh/graph>
    WHERE { 
            VALUES(?label) {%s}
            ?uri a 	meshv:Concept;
                 rdfs:label ?label. 
            }
    '''

    DOCUMENT_TYPE_MAP = {'Journal articles':       ['fabio:ResearchPaper', 'eprint:JournalArticle',
                                                    'schema:ScholarlyArticle', 'bibo:AcademicArticle'],                                  
                          'Conference papers':     ['fabio:ConferencePaper', 'eprint:ConferencePaper'],
                          'Poster communications': ['fabio:PosterPaper', 'eprint:ConferenceItem'], 
                          'Conference poster':     ['fabio:ConferencePoster', 'eprint:ConferencePoster'],
                          'Theses':                ['fabio:Thesis', 'eprint:Thesis', 'bibo:Thesis'],
                          'Preprints':             ['fabio:Preprint', 'eprint:SubmittedJournalArticle'],
                          'Videos':                ['fabio:MovingImage', 'bibo:AudioVisualDocument' ],
                          'Books':                 ['fabio:Book', 'eprint:Book', 'bibo:Book'],
                          'Book sections':         ['fabio:BookChapter', 'eprint:BookItem', 'bibo:BookSection'],
                          'Scientific blog post':  ['fabio:BlogPost'],
                          'Patents':               ['fabio:Patent', 'eprint:Patent', 'bibo:Patent'],
                          'Reports':               ['fabio:Report', 'eprint:Report', 'bibo:Report'],
                          'Other publications':    ['fabio:Expression', 'eprint:Text', 'bibo:Document']
    }

    BIBLIO_NAMESPACES = {'schema': 'http://schema.org/',
                        'fabio': 'http://purl.org/spar/fabio/',
                        'eprint': 'http://purl.org/eprint/type/',
                        'bibo': 'http://purl.org/ontology/bibo/',
    }

    PRE_PROCESSING_MAP = { }

    FIELD_PROCESSING_MAP = {'paper_id': ('extract_string', (PAPER_ID_REGEX,) ),

                            'year'    : [('extract_string', (YEAR_REGEX,)   ),
                                         ('ffill', {'downcast':'infer'}, )], 

                            'language': ('map_to_value', (LANG_MAP, LANG_MAP['default'] ), 'language_bib'), 

                            'types'    : ('take_at', (1,), 'type'),
                            'type'     : [('extract_string', (BEFORE_COMMA_REGEX,) ),
                                          ('map_to_value',  (DOCUMENT_TYPE_MAP, ), 'classes') ],

                            'classes'  : ('expand_prefix', (BIBLIO_NAMESPACES, ) ,), 
                                            
                            'sources'    : [('remove_from_list', (NON_SOURCES_REGEX,) ),
                                            ('take_first', (), 'publication')  ],

                            'rights'    : [ ('keep_in_list', (LICENSE_URI_REGEX,) , 'license'),
                                            ('keep_in_list', (ACCESS_REGEX,) , 'access_rights'),
                                            ('remove_from_list', (LICENSE_URI_REGEX,), ),
                                            ('remove_from_list', (ACCESS_REGEX,), )    
                                        ],

                            'access_rights' : ('take_first', (), ),

                            'relations' :  [ ('extract_string', (DOI_REGEX,), 'doi'),
                                             ('remove_from_list', (DOI_REGEX,), 'same_as')  ],

                            'doi' :        ('take_first', (), ),

                            'identifiers' :  [('keep_in_list', (HAL_URL_REGEX,), 'url'),
                                                ('keep_in_list', (PDF_URI_REGEX,), 'pdf_url')],
                                                
                            'url'     :   ('take_first', (),),
                            'pdf_url' :   ('take_first', (),),
  
                            'titles'      :  [('replace', (DOUBLE_QUOTES_REGEX, "'"), ),
                                            ('replace', (TIDY_TEXT_REGEX,), ) ],

                            'abstracts'      : [('replace', (DOUBLE_QUOTES_REGEX, "'"), ),
                                                ('replace', (TIDY_TEXT_REGEX,), ) ],

                            'subjects' : [('keep_in_list', (DOMAINS_SUBJECTS_REGEX,),  'domain_labels'),
                                        ('keep_in_list', (MESH_REGEX,),  'descriptor_labels'),] ,
                                        
                            'domain_labels' :  [('extract_string', (DOMAINS_SUBJECTS_REGEX, 1 ), 'domain_uris' ),
                                                ('replace', (r',', ';'), )],
                                           
                            'domain_uris'   : [ ('to_lower', (), ),
                                                ('prepend', (DOMAIN_NAMESPACE,), ) ],

                            'descriptor_labels': [('replace', (MESH_REGEX,), ) ,
                                                ('map_to_value_sparql', (MESH_SPARQL_WRAPPER, MESH_QUERY_TEMPLATE), 'descriptor_uris'),
                                                ('replace', (r',', ';'), ) ],

    }

    OPEN_ACCESS_FILTER = 'not access_rights.str.contains("closed|restricted|embargoed", case=False, na="OpenAccess", regex=True)'

    # instance specific processing function
    # TODO: possibly move to a separate module
    def select_part_text(row, textPart='title'):
        """ 
        Select text in a given language from a list of texts in different languages
        
        """
        doc_lang = row['language']
        part_text_list = row[f'{textPart}s'] if isinstance(row[f'{textPart}s'], list) else []
        part_lang_list = row[f'{textPart}s_lang'] if isinstance(row[f'{textPart}s_lang'], list) else []

        # zip lists into dictionary for easier access
        part_text_dict = dict(zip(part_lang_list, part_text_list))

        if part_text_dict and isinstance(part_text_dict, dict):
            if doc_lang in part_text_dict.keys():
                row[f'{textPart}'] = part_text_dict[doc_lang]
                row[f'{textPart}_lang'] = doc_lang
            elif len(part_text_dict) > 0:
                row[f'{textPart}'] = list(part_text_dict.values())[0]
                row[f'{textPart}_lang'] = list(part_text_dict.keys())[0]
            else:
                row[f'{textPart}'] = ''
                row[f'{textPart}_lang'] = ''

        return row 

    POST_PROCESSING_MAP = { 'select title' :    ('apply', { 'func' : select_part_text, 'args': ('title',) , 'axis':1} ),
                            'select abstract' : ('apply', { 'func' : select_part_text, 'args': ('abstract',) , 'axis':1} ),
                            'drop columns'  :   ('drop', {'axis':1 , 'columns': ['contributors', 'publishers', 'coverage',
                                                                                'types','sources',
                                                                                'relations', 'identifiers',
                                                                                'titles', 'titles_lang',
                                                                                'descriptions', 'abstracts', 'abstracts_lang',
                                                                                'subjects' ]} ), 
                            'filter open access' : ('query', {'expr': OPEN_ACCESS_FILTER } ), 
    }


class cfg_create_dataset_repository(cfg_pipeline):
    
    INPUT_PATH = cfg_process_corpus_metadata.OUTPUT_PATH
    INPUT_METADATA_FILENAME = cfg_process_corpus_metadata.PROCESSED_DATA_FILENAME
    RAW_METADATA_FILENAME = cfg_process_corpus_metadata.RAW_DATA_FILENAME

    DATASET_NAME = _ISSA_DATASET

    REMOVE_FILES = False
    SAVE_LABELS_TSV = False
    SAVE_PDF_URL = True
    SAVE_META_TEXT = False
    SAVE_META_JSON = True
    
    OUTPUT_SUFFIX = '.meta'
    
    JSON_SCHEMA={
        'paper_id' : '',
        'metadata' : {
            'doi': '',
            'title': '',
            'authors': '',
            'title_lang': {'code': '', 'score': 0.0},
            'abstract_lang': {'code': '', 'score': 0.0},
        },
        'abstract' : [{'text' : ''}],
    }
    
    METADATA_TO_JSON_MAP = {
        'paper_id'             : ['paper_id'],
        'doi'                  : ['metadata', 'doi'],
        'title'                : ['metadata', 'title'],
        'abstract'             : ['abstract', 0, 'text'],
        'authors'              : ['metadata', 'authors'],
        'title_lang'           : ['metadata', 'title_lang','code'] ,
        #'title_lang_score'     : ['metadata', 'title_lang','score'] ,
        'abstract_lang'        : ['metadata', 'abstract_lang','code'] ,
        #'abstract_lang_score'   : ['metadata', 'abstract_lang','score'] ,
    }
    

class cfg_openalex_data(cfg_pipeline):
    
    FILES_LOC = cfg_pipeline.FILES_LOC

    INPUT_PATTERN = '*.json'

    INPUT_PATH = FILES_LOC['metadata_json']

    DOCUMENT_URI_TEMPLATE = cfg_pipeline.DOCUMENT_URI_TEMPLATE
    
    SPARQL_PREFIXES = """
PREFIX bibo:   <http://purl.org/ontology/bibo/>
PREFIX dc:     <http://purl.org/dc/elements/1.1/>
PREFIX dce:    <http://purl.org/dc/elements/1.1/>
PREFIX dct:    <http://purl.org/dc/terms/>
PREFIX foaf:   <http://xmlns.com/foaf/0.1/>
PREFIX gn:     <http://www.geonames.org/ontology#>
PREFIX issapr: <http://data-issa.cirad.fr/property/>
PREFIX oa:     <http://www.w3.org/ns/oa#>
PREFIX rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wdt:    <http://www.wikidata.org/prop/direct/>
        """

    OPENALEX_API = {
        'base_url' : 'https://api.openalex.org/works/',
        'use_mailto' : True,           # use if special rate limit agreement with OpenAlex, denoted by param mailto in the API query
        'mailto': 'franck.michel@inria.fr',
        'max_workers' : 30,             # used if use_mailto = True, max number of parallel workers
        'pause_sequential' : 0.1,       # used if use_mailto = False, pause between two sequential invokations
        'pause_error' : 2.0             # pause when an error occurs
    }
    
    SERVICES = {
        'authorships':  "http://localhost:81/service/openalex/getAuthorshipsByDoi",
        'sdgs':         "http://localhost:81/service/openalex/getSdgsByDoi",
        'topics':       "http://localhost:81/service/openalex/getTopicsByDoi",
    }

    OUTPUT_FILES = {
        # Complementary metadata retrieval from SPARQL micro-services
        'authorships':      os.path.join(FILES_LOC['rdf'], "issa-document-openalex-authorships.ttl"),
        'sdgs':             os.path.join(FILES_LOC['rdf'], "issa-document-openalex-sdgs.ttl"),
        'topics':           os.path.join(FILES_LOC['rdf'], "issa-document-openalex-topics.ttl"),

        # Citation and topics data retrieval to compute the Rao-Stirling index
        'article_citation': os.path.join(FILES_LOC['openalex'], "article-citation-subjects.json"),
        'subject_citation_matrix': os.path.join(FILES_LOC['openalex'], "article-citation-subjects-matrix.json"),
        'rao_stirling_index': os.path.join(FILES_LOC['openalex'], "rao-stirling.json"),
        'rao_stirling_index_intervals': os.path.join(FILES_LOC['openalex'], "rao-stirling-intervals.json"),
    }

    # One of: "Topic", "Subfield", "Field", "Domain"
    RAO_STIRLING_CALC_LEVEL = "Subfield"

    # Sort Rao Stirling index values into intervals of this size
    RAO_STIRLING_INTERVAL = 0.01

    SAVE_SUBJECT_CITATION_MATRIX = True


class cfg_extract_text_from_pdf(cfg_pipeline):

    FILES_LOC = cfg_pipeline.FILES_LOC
    
    INPUT_PATH = FILES_LOC['pdf']
    INPUT_PATTERN = '*.url'
    
    OUTPUT_PATH = FILES_LOC['fulltext_json']
    OUTPUT_SUFFIX = '.grobid'
    OVERWRITE_EXISTING = True
    OUTPUT_IF_BAD_PDF = True
    
    CACHE_PDF = True
    CACHE_PATH =_PDF_CACHE
    CACHE_UNREADABLE_PATH =_PDF_CACHE_UNREADABLE
    
    SAVE_XML = True
    SAVE_TEXT= False  
    OUTPUT_XML_PATH = FILES_LOC['xml']
    OUTPUT_TXT_PATH = FILES_LOC['txt']  
    OUTPUT_PDF_PATH = FILES_LOC['pdf']
    
    DOWNLOAD_DELAY = 5 #sec

    GROBID_URL = 'http://localhost:8070'
    GROBID_API_URL = f'{GROBID_URL}/api/processFulltextDocument'
    GROBID_TIMEOUT = 300 #sec

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

    DO_INDEX = False


class cfg_indexing_postprocess(cfg_pipeline): 
   
    DO_INDEX = False


# Common config setting for the annotation scripts
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

    REQUEST_TIMEOUT = 120


class cfg_annotation_dbpedia(cfg_annotation): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    OUTPUT_PATH = FILES_LOC['annotation_dbpedia']
   
    SPOTLIGHT_ENDPOINTS = {
        # local API endpoints
        'en': 'http://localhost:2222/rest/annotate',
        'fr': 'http://localhost:2223/rest/annotate',
        # external API endpoints
        #'en': 'https://api.dbpedia-spotlight.org/en/annotate', 
        #'fr': 'https://api.dbpedia-spotlight.org/fr/annotate',
    }
    
    SPOTLIGHT_CONFIDENCE= 0.50
    SPOTLIGHT_SUPPORT   = 10


class cfg_annotation_wikidata(cfg_annotation): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    OUTPUT_PATH = FILES_LOC['annotation_wikidata']

    # Local API endpoint
    ENTITY_FISHING_ENDPOINT = 'http://localhost:8090/service/disambiguate'
    # External API endpoint
    #ENTITY_FISHING_ENDPOINT = 'https://cloud.science-miner.com/nerd/service/disambiguate'
    
    REMOVE_GLOBAL_CATEGORIES = True


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
        # local API endpoints   
        'disambiguation' : 'http://localhost:8090/service/disambiguate',
        'concept_lookup': 'http://localhost:8090/service/kb/concept'}
        # external API endpoints
        #'disambiguation' : 'https://cloud.science-miner.com/nerd//service/disambiguate/',
        #'concept_lookup': 'https://cloud.science-miner.com/nerd//service/kb/concept/',}

    USE_CACHE = True


class cfg_annotation_pyclinrec(cfg_annotation): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    OUTPUT_PATH = FILES_LOC['annotation_pyclinrec']
    
    PYCLINREC_ENDPOINT = 'http://localhost:5002/annotate'

    PYCLINREC_DICTIONARIES = ['mesh'] 
    
    PYCLINREC_CONFIDENCE= 0.15

    DO_ANNOTATE=True


class cfg_overlap_detection(cfg_pipeline): #cfg_pipeline
    FILES_LOC = cfg_pipeline.FILES_LOC    

    INPUT_PATTERN = '*.json'

    OUTPUT_SUFFIX = '.json'
    OUTPUT_OVERWRITE_EXISTING = True  

    # These variables will be assigned from the CONFIG_MAP in a loop
    # to keep a consistent processing pattern
    INPUT_PATH = None
    OUTPUT_PATH = None
    JSON_MAP = None    
  
    CONFIG_MAP= {'dbpedia' : {  'INPUT_PATH' : FILES_LOC['annotation_dbpedia'],
                                'OUTPUT_PATH' : FILES_LOC['annotation_dbpedia'],
                                            # json path to     terms                      text            offset     score              how
                                'JSON_MAP' : { 'title':     (['title', 'Resources'] ,    'surfaceForm', 'offset' , 'similarityScore', 'length'  ),
                                               'abstract':  (['abstract', 'Resources'],  'surfaceForm', 'offset' , 'similarityScore', 'length'  ),
                                               'body_text': (['body_text' ,'Resources'], 'surfaceForm', 'offset' , 'similarityScore', 'length'  )},
                             },
                 'mesh' : {   'INPUT_PATH' : FILES_LOC['annotation_pyclinrec'],
                                 'OUTPUT_PATH' : FILES_LOC['annotation_pyclinrec'],
                                 'JSON_MAP' :  { 'title':     (['title', 'concepts'] ,    'matched_text', 'start' , 'confidence_score', 'length'  ),
                                                 'abstract':  (['abstract', 'concepts'],  'matched_text', 'start' , 'confidence_score', 'length'  ),
                                                 'body_text': (['body_text' ,'concepts'], 'matched_text', 'start' , 'confidence_score', 'length'  )}
         }

    }

    ASYNCH_PROCESSING = True
    ASYNCH_MAX_WORKERS = 10

    REMOVE_OVERLAPS = False
