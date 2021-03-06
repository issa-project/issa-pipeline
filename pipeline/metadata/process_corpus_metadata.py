# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""
import os
import sys
import pandas as pd
from collections import OrderedDict
import datetime

sys.path.append('..')  

from config import cfg_process_corpus_metadata as cfg
from util import read_metadata, save_metadata
from util import open_timestamp_logger, close_timestamp_logger
from util import detect_lang

from logging import INFO, DEBUG

#%%
logger = open_timestamp_logger(log_prefix= os.path.splitext(os.path.basename(__file__))[0], 
                               log_dir=cfg.LOG_PATH, 
                               file_level=DEBUG if cfg.DEBUG else INFO,
                               first_line = 'Processing %s metadata file...' % cfg.RAW_DATA_FILENAME)
#%%
def remove_nans(df):
    """
    Remove records w/o proper URI and w/o assosciated PDF file 

    """
    # check if all the records have URIs
    logger.info('Dropping %d records with no URI:' % df.loc[df.uri.isna()].shape[0])
    logger.debug('\t'+ df.loc[df.uri.isna(), ['paper_id', 'datestamp','uri']].to_string().replace('\n', '\n\t')) 
    
    df.dropna(subset=['uri'] , inplace=True)
    
    return df

#%%
def filter_not_yet_processed_articles(df):
    """
    Remove articles w/o assosciated PDF file.
    They will be processed in the next ittertaion

    """
    
    # Check pdf URLs for articles and remove non-pdfs
    is_pdf_url = df.pdf_url.apply(lambda x: x.lower().endswith('.pdf')) | (df.type != 'article' )
    
    logger.info('Dropping %d article records with no pdf URL: ' , is_pdf_url[~is_pdf_url].shape[0])
    logger.debug('\t'+ df.loc[~is_pdf_url, ['paper_id', 'datestamp', 'uri', 'pdf_url']].to_string().replace('\n', '\n\t')) 
    
    df.drop( is_pdf_url[~is_pdf_url].index , inplace=True)
    
    return df

#%%

def extract_paper_id(df):
    """
    Parse the unique id from the OAI generated one 
    For ex., if paper_id= 'oai:agritrop.cirad.fr:6554' then paper_id=6554.

    """
    
    df.paper_id = df.paper_id.apply(lambda x : x.split(':')[-1])
    
    return df

def trim_abstract(df):
    """
    Replaaces the string (R??sum?? d'auteur) at the end of many abstracts 

    """
   
    df.abstract = df.abstract.str.replace("\(R??sum?? d'auteur\)" , '') \
                             .str.replace("\(R??sum?? d'auteurs\)" , '')
    
    return df 

def remove_tabs(df):
    """
    Title and abstract text can contain tabs. In this case parsing TSV file 
    may result in a field shift. 
    Unfortunately Pandas's save_csv does not take car of this.
    """
    
    df.title = df.title.str.replace("\t" , ' ')
    df.abstract = df.abstract.str.replace("\t" , ' ')
   
    return df

#%%
# ## Split descriptors on text and uri 

def get_descriptors_text(dl):
    """
    Helper function that separates text descriptors from the mixture 
    of text and uris that is returned from Agritriop

    Parameters
    ----------
    dl : list
        Descriptor list.

    Returns
    -------
    list
        list of text descritors only.
    """
    dl = list(filter(lambda x: x is not None , dl))
    return list(filter(lambda x: not x.startswith('http') , dl))

def get_descriptors_uris(dl):
    """
    Helper function that separates uri descriptors from the mixture 
    of text and uris that is returned from Agritriop

    Parameters
    ----------
    dl : list
        Descriptor list.

    Returns
    -------
    list
        list of uri descritors only.
    """
    dl = list(filter(lambda x: x is not None , dl))
    return list(filter(lambda x: x.startswith('http') , dl))

def remove_with_prefix(dl, prefix):
    """
    Helper function that removes string from the list that start with prefix

    Parameters
    ----------
    dl : list
        Descriptor list.

    Returns
    -------
    list
        updated list.
    """
    dl = list(filter(lambda x: x is not None , dl))
    return list(filter(lambda x: not x.startswith(prefix) , dl))

#TODO: split descriptors into 3 categories
def split_descriptors(df):
    """
    Separates text and uri descriptors from the mixture 
    of text and uris that is returned from Agritriop into two columns

    """
    logger.info('Splitting descriptors lists...')
    
    df.descriptors_uris = df.descriptors.apply(lambda x: get_descriptors_uris(x))
    df.descriptors = df.descriptors.apply(lambda x: get_descriptors_text(x))
    return df

#TODO: not the best solution, refactor 
def split_license(df, ignore_text='Cirad license', ignore_uri='https://agritrop.cirad.fr/mention_legale.html'):
    """
    Split license list on text and uri ignoring 'info:eu-repo...' 

    """
    def _extract_uri(dl):
        dl = get_descriptors_uris(dl)
        if ignore_uri is not None:
            dl = remove_with_prefix(dl, ignore_uri)
            
        return dl[0] if len(dl) > 0 else ''   
    
    def _extract_text(dl):
        dl = get_descriptors_text(dl)
        dl = remove_with_prefix(dl, 'info:')
        if ignore_text is not None:
            dl = remove_with_prefix(dl, ignore_text)
            
        return dl[0] if len(dl) > 0 else ''  
        
    df.license_uri = df.licenses.apply(lambda x: _extract_uri(x))
    df.license_text = df.licenses.apply(lambda x: _extract_text(x))
    
    return df

#%%
def split_relations(df):
    """
    OAI api provide field relations that have multiple meanings .
    This function extracts doi id and links other than agritrop's own'
    """
    
    doi_prefix = 'https://doi.org/'
    argritrop_prefix = 'http://agritrop.cirad.fr/'
    
    def _extract_doi(dl):
        dl = get_descriptors_uris(dl)
        
        dl = list(filter(lambda x: x.startswith(doi_prefix) , dl))

        return dl[0].replace(doi_prefix, '') if len(dl) > 0 else ''
    
    def _extract_same_as(dl):
        dl = get_descriptors_uris(dl)
        dl = remove_with_prefix(dl, argritrop_prefix)
        dl = remove_with_prefix(dl, doi_prefix)
        return dl

    df.doi = df.relations.apply(lambda x: _extract_doi(x))
    df.same_as = df.relations.apply(lambda x: _extract_same_as(x))
    
    return df

#%%
def drop_records_without_descriptors(df):
    """
    Drop the metadata records without the descriptors

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df : pandas.DataFrame
        Updated dataframe

    """
    
    uris_len = df.descriptors_uris.apply(len)
    
    logger.info('Dropping %d records with no descriptors: ' % df.loc[uris_len == 0].shape[0])
    logger.debug('\t'+ df.loc[uris_len == 0, ['paper_id', 'datestamp', 'uri', 'descriptors']].to_string().replace('\n', '\n\t')) 
    
    df.drop( df.loc[uris_len == 0].index , inplace=True)
    return df
       
#%%
def print_stats(df, verbose=True):
    """
    Print some dataframe stats

    Parameters
    ----------
    df : pd.DataFrame
    verbose : bool, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    df : pd.DataFrame
        returns the same dataframe to be used in pipes

    """

    logger.info('')
    logger.info('Documents In English: %d ', df[df.language=='eng'].shape[0])
    logger.info('Documents In French: %d', df[df.language=='fre'].shape[0])
    if verbose:      
        logger.info('')
        logger.info('URI Descriptors:')
        logger.info(df.descriptors_uris.explode().describe().loc[['count', 'unique', 'top', 'freq']])
        logger.info('Descriptors per document:')
        logger.info('min \t %d' , df.descriptors_uris.apply(len).min())
        logger.info('max \t %d' , df.descriptors_uris.apply(len).max())
        logger.info('median\t %d' , df.descriptors_uris.apply(len).median())
        logger.info('')
        logger.info('Geo descriptors:')
        logger.info(df.geo_descriptors.explode().describe().loc[['count', 'unique', 'top',  'freq']])
        logger.info('Geo descriptors per document:')
        logger.info('min \t %d' , df.geo_descriptors.apply(len).min())
        logger.info('max \t %d' , df.geo_descriptors.apply(len).max())
        logger.info('median\t %d' , df.geo_descriptors.apply(len).median())
        
    return df

#%%
def fill_iso_lang(df):
    """
    Fill the iso_lang with default language, used down the piplene in rdf creation
    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df :  pandas.DataFrame
        Updated dataframe.

    """
    df.iso_lang = df.language.apply(lambda l: cfg.LANG_MAP.get(l,  cfg.LANG_MAP['default']) )
    return df

def detect_lang_wrapper(text, hint=None):
    """
    Wraps the call to the language detection to return mappable pandas.Series
    of pair (lang, score)
    
    Parameters
    ----------
    text : string

    Returns
    -------
    pandas.Series
    """
    
    #hint = cfg.LANGUAGE if cfg.LANGUAGE != 'en' else None
    hint = hint if hint != 'en' else None

    bf = cfg.BEST_EFFORT_LANG_DETECTION
    lang, score = detect_lang(text, 
                              best_effort=bf, hint_language=hint, 
                              return_score=True, logger=logger )
    
    return pd.Series([lang, score])

def detect_title_lang(df):
    """
    Fill the title_lang column with language code detected by pycld2 l
    anguage detector

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df :  pandas.DataFrame
        Updated dataframe.

    """
   
    if cfg.DETECT_LANG:
        logger.info('Detecting title language...')
         
        df[['title_lang', 'title_lang_score']] = df.loc[:, ['title', 'iso_lang']] \
                                                   .fillna('') \
                                                   .apply(lambda x: detect_lang_wrapper(x.title, x.iso_lang), axis=1) 
         
    if cfg.FILL_NOT_DETECTED_LANG:
         df.title_lang.fillna(df.iso_lang, inplace=True)
         df.title_lang_score.fillna(0.0, inplace=True)

    return df

def detect_abstract_lang(df):
    """
    Fill the abstract_lang column with language code detected by pycld2 l
    anguage detector

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df :  pandas.DataFrame
        Updated dataframe.
    """

    if cfg.DETECT_LANG:
        logger.info('Detecting abstract language...')
    
        df[['abstract_lang', 'abstract_lang_score']] = df.abstract.fillna('').apply(detect_lang_wrapper)
      
    if cfg.FILL_NOT_DETECTED_LANG:
         df.abstract_lang.fillna(df.iso_lang, inplace=True)
         df.abstract_lang_score.fillna(0.0, inplace=True)

    return df
#TODO:remove
def _test_detect_lang():
    output_metadata_file = os.path.join(cfg.OUTPUT_PATH, cfg.PROCESSED_DATA_FILENAME)
    output_metadata_file = os.path.realpath(os.path.normpath(output_metadata_file))

    df = read_metadata(output_metadata_file)
    
    df = detect_title_lang(df)
    df = detect_abstract_lang(df)
    
    save_metadata(df, output_metadata_file)

#%%
def get_live_descriptors_labels(row, language='en'):
    """
    Query specific language lables for a given URI in a domain specific
    descriptors vocabulary

    Parameters
    ----------
    row : pandas.DataFrame row
        
    language : string, optional
        Lablel language. The default is 'en'.

    Returns
    -------
    dict
        Dictionary with URIs as keys and labels as values.

    """

    try:
        
        if row.descriptors_uris:
            uris = ['(<%s>)' % x for x in row.descriptors_uris]
            
            logger.debug('%s: %s', row.paper_id,  ','.join(uris))
            
            query = cfg.VOCAB_QUERY_TEMPLATE % (' '.join(uris) , language)
            
            res = cfg.VOCAB_SPARQL_WRAPPER.sparql_to_dataframe(query)
            
            #return dict(zip(res.uri, res.label))
            
            #preserve original order
            res_dict = dict(zip(res.uri, res.label))
            ret_dict = OrderedDict()
            for uri in row.descriptors_uris:
                try:
                    ret_dict[uri] = res_dict[uri]
                except KeyError:
                    logger.error('Cannot find label for <%s>', uri)
            
            return ret_dict

    except Exception as e:
        logger.exception(e)
        
    return {}
        
def compare_descr_lists (list1, list2):
    """
    Compare two descriptor lists

    """

    if len(list1) != len(list2):
        return False

    for i in range(0, len(list1)):
        if list1[i] != list2[i]:
            return False
    
    return True
#%%
def get_live_labels(df):
    """
    Refresh lables in specified language for descriptors' URIs

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    df :  pandas.DataFrame
        Updated dataframe.
    """
    
    logger.info('Getting descriptors labels...')
    #TODO: progress indicator
    
    res = df.apply(lambda r: get_live_descriptors_labels(r, r.iso_lang), axis=1)
    
    #update the uris because some of them cannot be reolved especially for French
    #and also to maintain the same order
    df.descriptors_uris   = res.apply(lambda x: list(x.keys()))
    df.descriptors_labels = res.apply(lambda x: list(x.values()))
    
    #df.descriptors =  res.apply(lambda x: [{'uri': k, 'lbl': v} for k,v in x.items()] )   
    
    return df

#%%
def add_date(df):
    """
    Store metadata processing date
    """
    df['proc_date'] = datetime.datetime.now().strftime('%d-%m-%Y')
    
    return df
    
#%%
def replace_doublequotes(df):
    """
    Replace double quotes in titles and abstracts.
    Double quotes cause problems in conversion to Turtle
    """
    
    df.title = df.title.fillna('').str.replace('""' , "'")
    df.abstract = df.abstract.fillna('').str.replace('"' , "'")
    
    return df

#%%
def fill_year(df):
    """
    Fill n/a with forward fill values for column 'year'.
    Otherwise it causes a casting problem in Mongo and further 
    in conversion to Turtle.
    """
    
    df.year = df.year.fillna(method='ffill', downcast='infer')
    
    return df
    
#%%
def process(save_file=True):
    """
    Run corpus metadata data processing
    
    Parameters
    ----------
    safe_file : boolean
        save processed matadata. Deafutl=true

    """
    input_metadata_file = os.path.join(cfg.INPUT_PATH, cfg.RAW_DATA_FILENAME)
    output_metadata_file = os.path.join(cfg.OUTPUT_PATH, cfg.PROCESSED_DATA_FILENAME)
    
    input_metadata_file = os.path.realpath(os.path.normpath(input_metadata_file))
    output_metadata_file = os.path.realpath(os.path.normpath(output_metadata_file))
    
    #try:
    df = (read_metadata(input_metadata_file)
          .pipe(remove_nans)
          .pipe(filter_not_yet_processed_articles)
          .pipe(extract_paper_id)
          .pipe(split_descriptors)
          .pipe(split_license)
          .pipe(split_relations)
          #.pipe(drop_records_without_descriptors)
          .pipe(trim_abstract)
          .pipe(remove_tabs)
          .pipe(replace_doublequotes)
          .pipe(fill_iso_lang)
          .pipe(detect_title_lang)
          .pipe(detect_abstract_lang)
          .pipe(get_live_labels) #TODO: consider moving this to the annif training part of the code
          .pipe(add_date)
          .pipe(fill_year)
          .pipe(print_stats, True)
          .pipe(save_metadata, output_metadata_file if save_file else None)
          )
    
    if save_file:
        logger.info('Dataset size = %d, saved in %s' % (df.shape[0], output_metadata_file) )
        

    #except Exception as e:
    #    logger.error(e)

    #return df

#%%     
if __name__ == '__main__':
    process()
    #test_detect_lang()

close_timestamp_logger(logger)


