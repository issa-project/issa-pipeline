# -*- coding: utf-8 -*-
""" 
@author: Quentin Scordo, Franck Michel
"""
import glob
import json
import os
import sys

sys.path.append("..")
from util import add_path_to_config
from util import open_timestamp_logger, close_timestamp_logger
from util import INFO, DEBUG
from openalex.common import *

add_path_to_config()
from config import cfg_openalex_data as cfg


# %% Set up logging
logger = open_timestamp_logger(
    log_prefix=os.path.splitext(os.path.basename(__file__))[0],
    log_dir=cfg.LOG_PATH,
    file_level=DEBUG if cfg.DEBUG else INFO,
)


# The variables below give the way the subject levels are spelled in the JSON file that gives the citation data
TOPIC = "Topic"
SUBFIELD = "Subfield"
FIELD = "Field"
DOMAIN = "Domain"


def fetch_document_list() -> list:
    """
    Retrieve the list of documents that have a DOI from the JSON metadata files

    Returns:
        list: list of dictionaries with keys 'paper_id' and 'doi'
    """

    metadata_files = glob.glob(os.path.join(cfg.INPUT_PATH, cfg.INPUT_PATTERN))
    logger.info(
        "Found %d files with pattern %s", len(metadata_files), cfg.INPUT_PATTERN
    )

    try:
        document_list = []
        for f_json in metadata_files:
            json_data = json.load(open(f_json))
            metadata = json_data["metadata"]
            if "doi" in metadata.keys() and metadata["doi"] != "":
                document_list.append(
                    {"paper_id": json_data["paper_id"], "doi": metadata["doi"]}
                )
                logger.info(f"{f_json}: DOI = {metadata['doi']}")
            else:
                logger.info(f"{f_json}: no DOI")

        return document_list
    except Exception as e:
        logger.error("Error in processing metadata: %s" % e)
        raise e


close_timestamp_logger(logger)
