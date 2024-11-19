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
_ISSA_DATA_ROOT	        = read_env_var('ISSA_DATA_ROOT' ,       os.path.expanduser('~/ISSA-2/data/agritrop') )
_ISSA_DATASET    	    = read_env_var('ISSA_DATASET' ,         'dataset-2-0')
_ISSA_LOG               = read_env_var('ISSA_PIPELINE_LOG',     '../logs')

_METADATA_PREFIX 	    = read_env_var('METADATA_PREFIX',       'agritrop_meta_test' )
_ANNIF_SUFFIX    	    = read_env_var('ANNIF_SUFFIX',          'annif')

_PDF_CACHE       	    = read_env_var('PDF_CACHE',             os.path.expanduser('~/ISSA-2/data/agritrop/pdf_cache') )
_PDF_CACHE_UNREADABLE   = read_env_var('PDF_CACHE_UNREADABLE',  os.path.expanduser('~/ISSA-2/data/agritrop/pdf_cache/unreadable'))

# Directories of data files relative to the LATEST_UPDATE_DIR

_REL_META 		        = read_env_var('REL_META',              '.' )
_REL_META_JSON 	        = read_env_var('REL_META_JSON',         'json/metadata')
_REL_PDF  		        = read_env_var('REL_PDF',               'pdf')

_REL_GROBID_XML  	    = read_env_var('REL_GROBID_XML',        'xml' )
_REL_GROBID_JSON  	    = read_env_var('REL_GROBID_JSON',       'json/fulltext')
_REL_COAL_JSON  	    = read_env_var('REL_COAL_JSON',         'json/coalesced')
_REL_OPENALEX 	        = read_env_var('REL_OPENALEX',          'openalex')

_REL_ANNIF_LABELS 	    = read_env_var('REL_ANNIF_LABELS',      'labels')
_REL_ANNIF_TEXT   	    = read_env_var('REL_ANNIF_TEXT',        'txt')
_REL_ANNIF		        = read_env_var('REL_ANNIF',             'indexing')

_REL_SPOTLIGHT	        = read_env_var('REL_SPOTLIGHT',         'annotation/dbpedia')
_REL_EF			        = read_env_var('REL_EF',                'annotation/wikidata')
_REL_GEONAMES		    = read_env_var('REL_GEONAMES',          'annotation/geonames')
_REL_PYCLINREC	        = read_env_var('REL_PYCLINREC',         'annotation/agrovoc')

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
               'openalex' :        os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_OPENALEX ),
               'rdf' :             os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_RDF ),
              
               'annotation_dbpedia': os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_SPOTLIGHT ),
               'annotation_wikidata':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_EF ),
               'annotation_geonames':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_GEONAMES ),
               #'annotation_agrovoc':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_PYCLINREC ),
               'annotation_pyclinrec':os.path.join(DATASET_ROOT_PATH, LATEST_UPDATE, _REL_PYCLINREC ),                      
               }
    
    USER_AGENT = 'ISSA extraction script' 

    # TSV metadata file where to look for new documents
    DOCUMENT_URI_TEMPLATE = 'http://data-issa.cirad.fr/document/%s'
    
    DEBUG=False    


class cfg_download_corpus_metadata(cfg_pipeline):

    OAI_DATASET_NAME = 'driver' 
    
    OAI_ENDPOINT_START = 'https://agritrop.cirad.fr/cgi/oai2?verb=ListRecords&metadataPrefix=oai_dc&set=%s'
    OAI_ENDPOINT_CONTINUE ='https://agritrop.cirad.fr/cgi/oai2?verb=ListRecords&resumptionToken=%s'
    #OAI_DELTA_RESUMPTION_TOKEN = 'metadataPrefix=oai_dc&offset=%s&set=%s'
    USER_AGENT = 'ISSA extraction script' 
    
    OAI_NS = {'oai': 'http://www.openarchives.org/OAI/2.0/', 
              'dc' : 'http://purl.org/dc/elements/1.1/',
              'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
              'xml': 'http://www.w3.org/XML/1998/namespace'}

    
    RAW_DATA_FILENAME = f'{_METADATA_PREFIX}.raw.tsv'
    OUTPUT_PATH = './output'

    SINGLE_FIELD_MAP = {'paper_id' : 'oai:header/oai:identifier',
                        'datestamp' :  'oai:header/oai:datestamp',
                        'url' : 'oai:metadata/oai_dc:dc/dc:identifier',
                        'type' : 'oai:metadata/oai_dc:dc/dc:type',
                        'publication' : 'oai:metadata/oai_dc:dc/dc:source',
                        'year' : 'oai:metadata/oai_dc:dc/dc:date',
                        'language_bib' : 'oai:metadata/oai_dc:dc/dc:language',
                        'title' : 'oai:metadata/oai_dc:dc/dc:title',
                        'abstract' : 'oai:metadata/oai_dc:dc/dc:description',
                        }
    
    MULTI_FIELD_MAP = {'authors' : 'oai:metadata/oai_dc:dc/dc:creator',
                       'subjects' : 'oai:metadata/oai_dc:dc/dc:subject',
                       'coverage' : 'oai:metadata/oai_dc:dc/dc:coverage',
                       'identifiers' : 'oai:metadata/oai_dc:dc/dc:identifier',
                       'rights' : 'oai:metadata/oai_dc:dc/dc:rights', 
                       'relations' : 'oai:metadata/oai_dc:dc/dc:relation',
                       'types' : 'oai:metadata/oai_dc:dc/dc:type',
                      }
    DEBUG = False


class cfg_process_corpus_metadata(cfg_pipeline):

    RAW_DATA_FILENAME = cfg_download_corpus_metadata.RAW_DATA_FILENAME 
    PROCESSED_DATA_FILENAME = f'{_METADATA_PREFIX}.tsv'
    
    INPUT_PATH = cfg_download_corpus_metadata.OUTPUT_PATH
    OUTPUT_PATH = INPUT_PATH
  
    AGROVOC_SPARQL_WRAPPER = SPARQL_Endpoint_Wrapper('https://data-issa.cirad.fr/sparql')
    
    # the mapping query have to follow a rule: the first returned variable is a lookup key, the second is a lookup value    
    AGROVOC_QUERY_TEMPLATE = '''
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
    LANG_DETECTION_METHOD = 'cld2' #  cld2 or langdetect, 
    BEST_EFFORT_LANG_DETECTION = False
    FILL_NOT_DETECTED_LANG = True


    PAPER_ID_REGEX = r'[^:]+$'
    YEAR_REGEX = r'\b\d{4}\b'

    JUNK_STRINGS_REGEX = r"(Résumé d'auteur)|(Résumé d'auteurs)" 


    DOI_REGEX = r'\b10\.\d{4,9}/[-.;()/:\w]+'
    URI_REGEX = r'\w+:(\/?\/?)[^\s]+'
    URL_REGEX = r'^https?:(\/?\/?)[^\s]+'

    DESCRIPTOR_URI_REGEX = r'^http:(\/?\/?)[^\s]+'
    DESCRIPTOR_NAMESPACE = 'http://agritrop.cirad.fr/'

    DOMAIN_CODE_REGEX = r'^[A-Z]\d{2}\b'
    DOMAIN_NAMESPACE = 'http://agrist.cirad.fr/agrist-thema/'

    BEFORE_COMMA_REGEX = r'[^\r\n,]+'
    TIDY_TEXT_REGEX = r'^\s+|\t|\n|\r|\s+$'
    DOUBLE_QUOTES_REGEX = r'"' # r'"{2,}'

    ACCESS_REGEX = r'^info:eu-repo/semantics.+'
    LICENSE_URI_REGEX = r'^https?:.+licenses.+'
    LEGAL_MENTION_REGEX = r'https://agritrop.cirad.fr/mention_legale.html'

    PDF_URI_REGEX = r'^https?:.+\.pdf$'

    AGRITROP_NAMESPACE = 'http://agritrop.cirad.fr/'

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
                'default': 'fr'}

    DOCUMENT_TYPE_MAP ={'article':          ['fabio:ResearchPaper', 'eprint:JournalArticle',
                                            'schema:ScholarlyArticle', 'bibo:AcademicArticle'],  
                        'application':      ['fabio:ComputerApplication'],                                
                        'conference_item':  ['fabio:ConferencePaper', 'eprint:ConferencePaper'],
                        'thesis':           ['fabio:Thesis', 'eprint:Thesis', 'bibo:Thesis'],
                        'pgd':              ['fabio:DataManagementPlan'],
                        'film':             ['fabio:Film', 'bibo:AudioVisualDocument' ],
                        'book':             ['fabio:Book', 'eprint:Book', 'bibo:Book'],
                        'book_section':     ['fabio:BookChapter', 'eprint:BookItem', 'bibo:BookSection'],
                        'map':              ['fabio:StillImage', 'bibo:Map'],
                        'patent':           ['fabio:Patent', 'eprint:Patent', 'bibo:Patent'],
                        'Reports':          ['fabio:Report', 'eprint:Report', 'bibo:Report'],
                        'monograph':        ['fabio:Expression', 'eprint:Text', 'bibo:Document'],
                        'revue':            ['fabio:Review'],
    }

    BIBLIO_NAMESPACES = {'schema':  'http://schema.org/',
                         'fabio':   'http://purl.org/spar/fabio/',
                         'eprint':  'http://purl.org/eprint/type/',
                         'bibo':    'http://purl.org/ontology/bibo/',
    }

    PRE_PROCESSING_MAP = {'drop unfinished documents' : ('dropna', {'subset': ['url']} ),
    }
    
    FIELD_PROCESSING_MAP = {'paper_id': ('extract_string', (PAPER_ID_REGEX,) ),
                            'year'    : [
                                            ('extract_string', (YEAR_REGEX,)   ),
                                            ('ffill', {'downcast':'infer'}, )   # this is a pandas method
                                        ], 
                            'language_bib': ('map_to_value', (LANG_MAP, LANG_MAP['default'] ), 'language'), 

                            'title'  :  [
                                            ('replace', (DOUBLE_QUOTES_REGEX, "'"), ),
                                            ('replace', (TIDY_TEXT_REGEX, ''), ),
                                            ('detect_language', (None, np.NaN), ['title_lang', 'title_lang_score'] ),
                                        ],
                            'abstract': [
                                            ('replace', (DOUBLE_QUOTES_REGEX, "'"), ),
                                            ('replace', (TIDY_TEXT_REGEX, ''), ),
                                            ('replace', (JUNK_STRINGS_REGEX, ''), ),
                                            ('detect_language', (None, np.NaN), ['abstract_lang', 'abstract_lang_score'] ),
                                        ],

                            'subjects':[
                                            ('keep_in_list', (URI_REGEX,) , 'descriptor_uris'), 
                                            ('keep_in_list', (DOMAIN_CODE_REGEX,) , 'domain_labels') ,
                                        ],


                            'domain_labels': ('extract_string',  (DOMAIN_CODE_REGEX,), 'domain_uris'),                 

                            'domain_uris'  : ( 'prepend', (DOMAIN_NAMESPACE, ), ), 

                            'rights'    : [
                                                ('keep_in_list', (LICENSE_URI_REGEX,) , 'license'), 
                                                ('keep_in_list', (ACCESS_REGEX,) , 'access_rights'), 
                                                ('keep_in_list', (LEGAL_MENTION_REGEX,),  )  
                                            ],

                            'access_rights' : ('take_first', (), ),

                            'relations' :   [
                                                ('extract_string', (DOI_REGEX,), 'doi'),
                                                ('remove_from_list', (DOI_REGEX,), 'same_as')  
                                            ],
                            'doi' :         ('take_first', (), ),
                            'same_as' :     [
                                                ('remove_from_list', (AGRITROP_NAMESPACE,) ),
                                                ('keep_in_list', (URL_REGEX,) )
                                            ],

                            'type'     :    ('map_to_value', (DOCUMENT_TYPE_MAP, ), 'classes'),
                            'classes'  :    ('expand_prefix', (BIBLIO_NAMESPACES, ) ,) , 


                            'identifiers' :  [('keep_in_list', (PDF_URI_REGEX,), 'pdf_url')],
                            'pdf_url' :   ('take_last', (),),
    }

    OPEN_ACCESS_FILTER = 'not access_rights.str.contains("closed|restricted|embargoed", case=False, na="OpenAccess", regex=True)'
  
    # Agrovoc dataset specific processing of the metadata that requires input from multiple columns
    def fillna_with_doc_language(row):
        row.loc[['abstract_lang', 'title_lang']] = row.loc[['abstract_lang', 'title_lang']].fillna(row['language'])
        return row
   

    def remove_pdfs_from_non_articles(row):
        if row['type'] != 'article':
            row['pdf_url'] = np.NaN
        return row
    
    def map_descriptor_labels (row):

        row['descriptor_labels'] = []
        
        if row['descriptor_uris']:
            uris = ' '.join(['(<%s>)' % uri for uri in row['descriptor_uris']])
            query = cfg_process_corpus_metadata.AGROVOC_QUERY_TEMPLATE % (uris, row['language'])
            result=  cfg_process_corpus_metadata.AGROVOC_SPARQL_WRAPPER.sparql_to_dataframe(query)
        
            # preserve original order
            res_dict = dict(zip(result.iloc[:, 0], result.iloc[:, 1]))
            row['descriptor_labels'] = [res_dict.get(uri, '') for uri in row['descriptor_uris']]


        return row

    POST_PROCESSING_MAP = { 'drop columns'  :   ('drop', {'axis':1 , 'columns': ['identifiers', 'relations', 'types' ]} ), 
                            'filter open access':             ('query',   {'expr': OPEN_ACCESS_FILTER } ), 
                            'fill lang na'       :            ('apply', {'func': fillna_with_doc_language , 'axis' : 1} ),
                            'remove PDFs from non-articles' : ('apply', {'func': remove_pdfs_from_non_articles, 'axis' : 1} ),  
                            'map descriptor labels' :         ('apply', {'func': map_descriptor_labels, 'axis' : 1} ),                  
    }


class cfg_create_dataset_repository(cfg_pipeline):
    
    INPUT_PATH = cfg_process_corpus_metadata.OUTPUT_PATH
    INPUT_METADATA_FILENAME = cfg_process_corpus_metadata.PROCESSED_DATA_FILENAME
    RAW_METADATA_FILENAME = cfg_process_corpus_metadata.RAW_DATA_FILENAME

    DATASET_NAME = _ISSA_DATASET

    REMOVE_FILES = False
    SAVE_LABELS_TSV = True
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
        'title_lang_score'     : ['metadata', 'title_lang','score'] ,
        'abstract_lang'        : ['metadata', 'abstract_lang','code'] ,
        'abstract_lang_score'  : ['metadata', 'abstract_lang','score'] ,
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
        'subject_citation_matrix': os.path.join(FILES_LOC['openalex'], "subject-citation-matrix.json"),
        'rao_stirling_index': os.path.join(FILES_LOC['openalex'], "rao-stirling-subject.json"),
        'rao_stirling_index_intervals': os.path.join(FILES_LOC['openalex'], "rao-stirling-subject-intervals.json"),
    }

    # One of: "Topic", "Subfield", "Field", "Domain"
    RAO_STIRLING_CALC_LEVEL = "Topic"

    # Sort Rao Stirling index values into intervals of this size
    RAO_STIRLING_INTERVAL = 0.1

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
                    #'keywords':  (['metadata', 'keywords'],  ['metadata', 'body_lang', 'code']),
                    'body_text': (['body_text' , 0, 'text'], ['metadata', 'body_lang', 'code']) 
        
                   }
    # order in which determine a document language
    LANGUAGE_DETERMINERS = ['body_text', 'abstract', 'title']

    DO_INDEX = True


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
    
    DO_INDEX = True


# This config may go somewhere else because this step is not a part of the 
# pipeline. Try to keep it independent    
class cfg_indexing_training(cfg_pipeline):
    
    LOG_PATH = '../logs' 
    
    INPUT_PATH=os.path.join(_ISSA_DATA_ROOT, _ISSA_DATASET)
    INPUT_PATTERN = '**/coalesced/*.json'
    LABEL_PATTERN='**/labels/'
    
    CREATE_LABELS = True
    METADATA_FILENAME=f'{_METADATA_PREFIX}.tsv'

    OUTPUT_SUFFIX = '.txt'
    
    PARTS_SEPARATOR = os.linesep + os.linesep
     
    OUTPUT_PATH = os.path.join(_ISSA_DATA_ROOT, 'training')
    
    TRAINING_FILES_LOC = {'en' : { 'train' : os.path.join(OUTPUT_PATH, 'en', 'train'),
                                   'test'  : os.path.join(OUTPUT_PATH, 'en', 'test') },
                          'fr' : { 'train' : os.path.join(OUTPUT_PATH, 'fr', 'train'),
                                   'test'  : os.path.join(OUTPUT_PATH, 'fr', 'test') }
                          }

    # json path to                 text                      language      
    JSON_TEXT_MAP= { 'title':    (['metadata', 'title'],     ['metadata', 'title_lang']),
                    'abstract':  (['abstract', 0, 'text'],   ['metadata', 'abstract_lang']),
                    #'keywords':  (['metadata', 'keywords'],  ['metadata', 'body_lang']),
                    'body_text': (['body_text' , 0, 'text'], ['metadata', 'body_lang'])  
                   }
    # order in which to determine a document language
    LANGUAGE_DETERMINERS = ['body_text', 'abstract'] #, 'title']
    LANGUAGE_SCORE_THRESHOLD = 0.75
    
    MIN_TEXT_LENGTH = 240
    PARTS_SEPARATOR = os.linesep + os.linesep
    FILES_SORT_KEY = lambda x: int(os.path.basename(x).split('.')[0]) # str.lower (alphabetical)
    FILES_SET_SIZE = 25000
    TEST_SET_SPLIT = 0.2


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


#class cfg_annotation_agrovoc(cfg_annotation): 
#    FILES_LOC = cfg_pipeline.FILES_LOC    

#    OUTPUT_PATH = FILES_LOC['annotation_agrovoc']
    
#    PYCLINREC_ENDPOINT = 'http://localhost:5000/annotate'
    
#    PYCLINREC_CONFIDENCE= 0.15

class cfg_annotation_pyclinrec(cfg_annotation): 
    FILES_LOC = cfg_pipeline.FILES_LOC    

    OUTPUT_PATH = FILES_LOC['annotation_pyclinrec']
    
    PYCLINREC_ENDPOINT = 'http://localhost:5002/annotate'

    PYCLINREC_DICTIONARIES = ['agrovoc'] 
    
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
                 'agrovoc' : {   'INPUT_PATH' : FILES_LOC['annotation_pyclinrec'],
                                 'OUTPUT_PATH' : FILES_LOC['annotation_pyclinrec'],
                                 'JSON_MAP' :  { 'title':     (['title', 'concepts'] ,    'matched_text', 'start' , 'confidence_score', 'length'  ),
                                                 'abstract':  (['abstract', 'concepts'],  'matched_text', 'start' , 'confidence_score', 'length'  ),
                                                 'body_text': (['body_text' ,'concepts'], 'matched_text', 'start' , 'confidence_score', 'length'  )}
                }
    }

    ASYNCH_PROCESSING = True
    ASYNCH_MAX_WORKERS = 10

    REMOVE_OVERLAPS = False
