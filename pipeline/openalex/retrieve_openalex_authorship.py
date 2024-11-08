# -*- coding: utf-8 -*-
""" 

@author: Franck Michel
"""
import os
import sys
import requests
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote, urlencode


sys.path.append("..")
from util import read_metadata
from util import open_timestamp_logger, close_timestamp_logger, INFO, DEBUG
from util import add_path_to_config

add_path_to_config()
from config import cfg_openalex_data as cfg

# %% Set up logging
logger = open_timestamp_logger(
    log_prefix=os.path.splitext(os.path.basename(__file__))[0],
    log_dir=cfg.LOG_PATH,
    file_level=DEBUG if cfg.DEBUG else INFO,
)


def fetch_doi_list():
    """
    Retrieve the list of DOIs from the metadata file (keep only articles with a DOI)

    Returns:
        list: list of dictionaries with keys 'paper_id' and 'doi'
    """
    metadata_file = os.path.join(cfg.INPUT_PATH, cfg.METADATA_FILENAME)
    logger.info("Processing %s metadata file..." % metadata_file)

    try:
        df = read_metadata(metadata_file)
        doi_list = df.loc[df["doi"].notnull(), ["doi", "paper_id"]].to_dict(
            orient="records"
        )
        return doi_list[:10]  # TODO remove the limit 5
    except Exception as e:
        logger.error("Error in processing metadata: %s" % e)
        raise e


def fetch_data(document_uri, doi) -> str:
    """
    Fetch authorship data for a given DOI and document URI
    from the SPARQL microservice

    Args:
        document_uri (str): document URI
        doi (str): document DOI

    Returns:
       str: RDF data in Turtle format
    """
    try:
        encoded_document_uri = quote(document_uri, safe="")
        encoded_doi = quote(doi, safe="")
        sparql_query = cfg.SPARQL_PREFIXES + " CONSTRUCT WHERE { ?s ?p ?o. }"
        encoded_sparql_query = urlencode({"query": sparql_query})
        url = f"{cfg.SERVICES['authorships']}?documentUri={encoded_document_uri}&documentDoi={encoded_doi}&{encoded_sparql_query}"

        logger.debug(f"Fetching authorship data for {document_uri}, DOI {doi}")
        response = requests.get(url, headers={"Accept": "text/turtle"})
        response.raise_for_status()
        return response.text

    except requests.exceptions.HTTPError as e:
        logger.error(f"Could not retrieve authorship for document {document_uri}, DOI {doi}: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Could not retrieve authorship for document {document_uri}, DOI {doi}: {e}")
        return None


# %% Main processing loop
if __name__ == "__main__":

    # Initialize lists and counters
    rdf_results = []
    error_count = 0

    # Fetch DOI list and document URIs
    document_list = fetch_doi_list()
    logger.info(f"No. of documents with a DOI: {len(document_list)}")

    if cfg.OPENALEX_API["use_mailto"]:
        # Parallel execution with ThreadPoolExecutor
        logger.info(f"Running with {cfg.OPENALEX_API['max_workers']} workers")
        with ThreadPoolExecutor(
            max_workers=cfg.OPENALEX_API["max_workers"]
        ) as executor:
            future_to_doi = {
                executor.submit(
                    fetch_data,
                    cfg.DOCUMENT_URI_TEMPLATE % item["paper_id"],
                    item["doi"],
                ): (
                    cfg.DOCUMENT_URI_TEMPLATE % item["paper_id"],
                    item["doi"],
                )
                for item in document_list
            }
            for future in tqdm(as_completed(future_to_doi), total=len(document_list)):
                document_uri, doi = future_to_doi[future]
                try:
                    rdf_data = future.result()
                    if rdf_data:
                        rdf_results.append(rdf_data)
                        logger.debug(f"Recorded authorship data for {document_uri}, DOI {doi}")
                    else:
                        error_count += 1
                except Exception as exc:
                    logger.error(f"Exception while processing document {document_uri}, DOI {doi}: {exc}")
                    error_count += 1
    else:
        # Sequential execution
        logger.info("Running in sequential execution mode")
        for item in document_list:
            (doi, paper_id) = (item["doi"], item["paper_id"])
            document_uri = cfg.DOCUMENT_URI_TEMPLATE % paper_id
            try:
                rdf_data = fetch_data(document_uri, doi)
                if rdf_data:
                    rdf_results.append(rdf_data)
                    logger.debug(f"Recorded authorship data for {document_uri}, DOI {doi}")
                else:
                    error_count += 1
            except Exception as exc:
                logger.error(f"Exception while processing DOI {doi} : {exc}")
                error_count += 1
            time.sleep(cfg.OPENALEX_API["pause_duration"])

    # Save RDF results to a Turtle file
    output = cfg.OUTPUT_FILES['authorship_data']
    with open(output, "w", encoding="utf-8") as rdf_file:
        rdf_file.write(cfg.SPARQL_PREFIXES)
        for rdf_data in rdf_results:
            for line in rdf_data.splitlines():
                if not line.startswith("@prefix"):
                    rdf_file.write(line + "\n")

    # Summary logging
    logger.info(f"Authorship data saved in {output}")
    logger.info(f"Number of successful records: {len(rdf_results)}")
    logger.info(f"Number of errors: {error_count}")

close_timestamp_logger(logger)
