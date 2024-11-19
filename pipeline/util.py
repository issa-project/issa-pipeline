# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:35:35 2021

@author: abobashe
"""
import os
import datetime
import logging
from copy import deepcopy
import sys


# %%
def add_path_to_config():
    """
    Config module by default is in the same directory as this module
    but it can be moved to a different location and the location should be passed
    as a first argument to a script that requires config
    """
    if len(sys.argv) > 1:
        sys.path.append(sys.argv[1])


# %%
# Functions to set up uniform logging with attached time stamp

# Propagate logging levels for caller modules convenience
INFO = logging.INFO
DEBUG = logging.DEBUG
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


def always_log_exceptions(exctype, value, tb):
    """
    Log uncaught exceptions with stack trace used as a hook for sys.excepthook

    Parameters:
        exctype : type, exception type
        value : exception, exception value
        tb : traceback, exception traceback

    Returns:
        None
    """
    # get the last logger in the list of loggers in hope that this is the one we need
    # TODO:refactor
    logger = [logging.getLogger(name) for name in logging.root.manager.loggerDict][-1]

    logger.exception("Uncaught exception", exc_info=(exctype, value, tb))


def open_timestamp_logger(
    log_prefix=None,
    log_dir=None,
    first_line=None,
    console_level=logging.INFO,
    file_level=logging.DEBUG,
):
    """
    Create a logger with a time stamp and optionally write to a file

    Parameters:
        log_prefix : str, optional prefix for the log file name. The default is None.
        log_dir : str, optional directory to save the log file. The default is None meaning no file is saved.
        first_line : str, optional first line to output to the log file like a log title. The default is None.
        console_level : logging level, optional logging level for console output. The default is logging.INFO.
        file_level : logging level, optional logging level for file output. The default is logging.DEBUG.

    Returns:
        logger : logging.Logger
    """
    logger = logging.getLogger(log_prefix)
    logger.setLevel(file_level)

    # remove all previously created streams to begin a new one
    if logger.hasHandlers():
        for i in range(len(logger.handlers) - 1, -1, -1):
            handler = logger.handlers[i]
            handler.close()
            logger.removeHandler(handler)

    # create a console handler with a higher log level
    console = logging.StreamHandler()
    console.setLevel(console_level)
    logger.addHandler(console)

    # create log dir
    if log_dir is not None:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    # create file handler with a lower log level
    if log_prefix is not None:
        fname = "%s_%s.log" % (
            log_prefix,
            datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
        )
        log_file = logging.FileHandler(os.path.join(log_dir, fname))
        log_file.setLevel(file_level)
        log_file.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)-8s %(message)s", datefmt="%d/%m/%Y %H:%M:%S"
            )
        )
        logger.addHandler(log_file)

    # output a line
    if first_line is not None:
        logger.info(first_line)

    sys.excepthook = always_log_exceptions

    return logger


def close_timestamp_logger(logger):
    """
    Close the logger and remove all handlers
    """
    logging.shutdown()


# %%
# Functions to read and save metadata files in TSV format with some column manipulation
import ast
import pandas as pd


def read_metadata(filePath):
    """
    Read a raw or processed metadata file converting columns into lists when
    necessary

    Parameters:
        filePath : str, path to the metadata file

    Returns:
        df : pandas.DataFrame
    """
    df = pd.read_csv(filePath, sep="\t", encoding="utf-8")
    # df = pd.read_csv(filePath, sep='\t', encoding='utf-8',
    #                 doublequote=False, escapechar="\\" )

    for col in df.columns:
        try:
            # convert some columns to lists
            df[col] = df[col].apply(ast.literal_eval)
        except:
            pass

    return df


def save_metadata(df, filePath):
    """
    Save processed DataFrame to a TSV file

    Parameters:
        df : pandas.DataFrame
        filePath : str, path to the metadata file

    Returns:
        df : pandas.DataFrame
    """
    if filePath is not None:

        if not os.path.exists(os.path.dirname(filePath)):
            os.makedirs(os.path.dirname(filePath))

        df.to_csv(filePath, sep="\t", encoding="utf-8", index=False)
        # df.to_csv(filePath, sep='\t', encoding='utf-8', index=False,
        #          doublequote=False, escapechar="\\" )

    return df


# %%
# Functions to read and save dictionary in JSON format
import json


def read_paper_json(json_path):
    """
    Read a JSON file into a dictionary

    Parameters:
        json_path : str, path to the JSON file

    Returns:
        json_dict : dict
    """
    json_path = os.path.realpath(os.path.normpath(json_path))
    with open(json_path, "r", encoding="utf-8", errors="ignore") as json_file:
        json_dict = json.load(json_file)

    return json_dict


def save_paper_json(json_path, json_dict):
    """
    Save a dictionary to a JSON file

    Parameters:
        json_path : str, path to the JSON file
        json_dict : dict

    Returns:
        None
    """
    json_path = os.path.realpath(os.path.normpath(json_path))

    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(json_dict, json_file, indent=4, ensure_ascii=False)


# %%
# Convinience functions to manipulate files and file attributes
import shutil


def copy_file(file_path, to_folder):
    """
    Copy a file to a folder

    Parameters:
        file_path : str, path to the file
        to_folder : str, path to the destination folder

    Returns:
        dest_file_path : str, path to the destination file
    """
    dest_file_path = os.path.join(to_folder, os.path.basename(file_path))
    shutil.copyfile(file_path, dest_file_path)

    return dest_file_path


def move_file(file_path, to_folder):
    """
    Move a file to a folder

    Parameters:
        file_path : str, path to the file
        to_folder : str, path to the destination folder

    Returns:
        dest_file_path : str, path to the destination file
    """
    dest_file_path = os.path.join(to_folder, os.path.basename(file_path))
    shutil.move(file_path, dest_file_path)

    return dest_file_path


def set_file_readonly(file_path, readonly=True):
    """
    Set file read only attribute

    Parameters:
        file_path : str, path to the file
        readonly : bool, True to set read only attribute, False to unset

    Returns:
        None
    """
    if readonly:
        os.chmod(file_path, 0o444)
    else:
        os.chmod(file_path, 0o666)


# %%
# Helper functions to detect language of the text

try:
    import pycld2 as cld2
except:
    # There is no implementation of pycld2 package for Windows
    # Fake it on Windows for compatibility defaulting to English
    class cld2(object):
        def detect(text, hintLanguage=None, bestEffort=False):
            isReliable = True
            textBytesFound = len(text)
            details = (
                ("ENGLISH", "en", 99, 100.0),
                ("Unknown", "un", 0, 0.0),
                ("Unknown", "un", 0, 0.0),
            )
            return isReliable, textBytesFound, details


def detect_lang(
    text,
    hint_language=None,
    best_effort=False,
    all_details=False,
    return_score=False,
    logger=None,
):
    """
    Detect language of the text using pycld2

    Parameters:
        text : string, text to detect language for
        hint_language : string, optional language code in ISO 639-1 format
        best_effort : bool, optional if True then try to detect language even if
                        detection is not reliable. The default is False.
        all_details : bool, optional if True and more thaan one language is detetced
                        return all of the languages separated by comma.
                        If False alsways return the first detected language
                        The default is False.
        return_score : bool, optional if True then return the score of the detection
                        The default is False.
        logger : logging.Logger, optional if specified then the details of language
                        detection will be logged. The defaoult is None

    Returns:
        lang : str or None, if detection is reliable then return string of detected
                        language code in ISO 639-1 format.
        score : float or None, if return_score is True then return the score of the detection
    """

    isReliable, textBytesFound, details = cld2.detect(text, hintLanguage=hint_language)

    if logger:
        logger.debug(text[:500])
        logger.debug(details)

    if not isReliable and best_effort:
        isReliable, textBytesFound, details = cld2.detect(
            text, hintLanguage=hint_language, bestEffort=True
        )
        if logger:
            logger.debug("best effort")
            logger.debug(details)

    lang = None
    score = None

    if isReliable:
        lang = details[0][1]
        score = details[0][2] / 100.0

        # typically the first language is good enough to return if more details
        # are needed use the details parameter
        if all_details and details[1][2] > 0:
            lang = ",".join([lang, details[1][1], details[2][1]])

    if return_score:
        return lang, score
    else:
        return lang


# %%
# Helper functions to manipulate nested dictionaries


def get_nested_dict_value(nested_dict, path_list, default=None):
    """
    Fetch the value from a dictionary provided the path as list of strings
    and indices

    Parameters:
        nested_dict : dict
        path_list : list, list of list of strings and/or indices
        default : any type, optional default value to return if key is not found

    Returns:
        value : any type
    """

    try:

        value = nested_dict
        for k in path_list:
            value = value[k]

    except KeyError:
        if default is not None:
            value = default
        else:
            raise

    return value


def set_nested_dict_value(nested_dict, path_list, value):
    """
    Assign value to a key mapped by path as list of strings and indices.
    Creates list if an index in a path os 0 but nested value is empty.
    In other cases if index is out of range then exception will be thrown.

    Parameters:
        nested_dict : dict, dictionary to update
        path_list : list of strings and/or indices
        value : any type of value to assign

    Return:
        nested_dict : dict,  updated dictionary
    """

    d = nested_dict
    for k in path_list[:-1]:
        if k == 0 and len(d) == 0:
            # create list for index=0 if list does not exist
            d = []
        d = d[k]

    d[path_list[-1]] = value

    return nested_dict


# inspired by post
# https://gist.github.com/angstwad/bf22d1822c38a92ec0a9?permalink_comment_id=4038517#gistcomment-4038517
def merge_nested_dicts(dict_a: dict, dict_b: dict):
    """
    Recursively merge nested dictionaries. The values of the second dictionary
    will overwrite the values for the same key in first dictionary.

    Parameters:
        dict_a : dict, first dictionary to merge
        dict_b : dict,  second dictionary to merge

    Return:
        result : dict,  merged dictionary
    """
    result = deepcopy(dict_a)
    for bk, bv in dict_b.items():
        av = result.get(bk)
        if isinstance(av, dict) and isinstance(bv, dict):
            result[bk] = merge_nested_dicts(av, bv)
        else:
            result[bk] = deepcopy(bv)
    return result


# %%
# Helper class to wrap SPARQL endpoint
from retrying import retry
from SPARQLWrapper import SPARQLWrapper, JSON  # , DIGEST, TURTLE, N3, XML, JSONLD
import pandas as pd
import json


class SPARQL_Endpoint_Wrapper(object):
    # TODO: add languages support

    def __init__(self, endpoint="http://localhost/sparql", timeout=0):
        self.sparql_wrapper = SPARQLWrapper(endpoint)
        self.sparql_wrapper.addParameter("timeout", str(timeout))

    @retry(
        stop_max_delay=10000,
        stop_max_attempt_number=5,
        wait_random_min=10,
        wait_random_max=2000,
    )
    def sparql_to_dataframe(self, query):
        """
                Helper function to convert SPARQL results into a Pandas data frame.
                Credit to Ted Lawless https://lawlesst.github.io/notebook/sparql-dataframe.html

        Parameters:
            query : str, SPARQL query

        Returns:
            df : pandas.DataFrame
        """

        self.sparql_wrapper.setQuery(query)
        self.sparql_wrapper.setReturnFormat(JSON)
        result = self.sparql_wrapper.query()

        processed_results = json.load(result.response)
        cols = processed_results["head"]["vars"]

        out = []
        for row in processed_results["results"]["bindings"]:
            item = []
            for c in cols:
                item.append(row.get(c, {}).get("value"))
            out.append(item)

        return pd.DataFrame(out, columns=cols)


# %%
# Helper functions to read environment variables
def read_env_var(var_name, default=None) -> str:
    """
    Read environment variable or return default value

    Parameters:
        var_name : str, name of the environment variable
        default : any type, optional default value to return if key is not found

    Returns:
        value : str
    """
    return os.environ[var_name] if var_name in os.environ else default
