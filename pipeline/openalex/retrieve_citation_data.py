# -*- coding: utf-8 -*-
""" 
Retrieve from OpenAlex, for each document with A DOI: 
its subjects (topic/subfield/field/domain), the cired articles,
and the subjects of the cited articles. The results are stored in a JSON file.
Later on, this is used to compute the Rao-Stirling interdisciplinarity index.

This script is invoked with one command line argument: the path
the path to the configuration file containing the class cfg_openalex_data

@author: Quentin Scordo, Franck Michel
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import requests
from traceback import format_exc
import time
from tqdm import tqdm
import sys

sys.path.append("..")
from util import add_path_to_config
from util import open_timestamp_logger, close_timestamp_logger
from util import INFO, DEBUG
from openalex.common import fetch_document_list, TOPIC, SUBFIELD, FIELD, DOMAIN

add_path_to_config()
from config import cfg_openalex_data as cfg

# %% Set up logging
logger = open_timestamp_logger(
    log_prefix=os.path.splitext(os.path.basename(__file__))[0],
    log_dir=cfg.LOG_PATH,
    file_level=DEBUG if cfg.DEBUG else INFO,
)


ERROR_404 = "Error HTTP status 404"
ERROR_OTHER = "Other error"


# Cache to avoid redundant API requests
article_cache = {}


def fetch_article(identifier) -> dict:
    """
    Fetch article info from the OpenAlex API

    Args:
        identifier (str): article identifier, DOI or OpenAlex id

    Returns:
        dict: article information (JSON response from OpenAlex API) or a simple string in case of an error
    """

    if "openalex.org" in identifier:
        _identifier = identifier
    else:
        _identifier = f"https://doi.org/{identifier}"
    logger.info(f"Fetching data for article {_identifier}")

    if _identifier in article_cache:
        return article_cache[_identifier]

    url = f"{cfg.OPENALEX_API['base_url']}{_identifier}"
    if cfg.OPENALEX_API["use_mailto"]:
        url += f"?mailto={cfg.OPENALEX_API['mailto']}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        article_cache[_identifier] = response.json()
        return article_cache[_identifier]

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            logger.warning("Rate limit reached. Sleeping for 20 seconds...")
            time.sleep(20)
            # TODO: manage max number of attempts
            return fetch_article(identifier)
        elif e.response.status_code == 404:
            return ERROR_404
        else:
            logger.warning(f"Error fetching article {_identifier}: {e}")
            return ERROR_OTHER
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request failed for article {_identifier}: {e}")
        return ERROR_OTHER


def reshape_article_data(article_info) -> dict:
    """
    Reshape the response from OpenAlex by keeping only relevant pieces of data

    Args:
        article_info (dict): article information from OpenAlex API

    Returns:
        dict: reshaped relevant article data
    """
    if article_info in [ERROR_404, ERROR_OTHER]:
        return None
    try:
        article_data = {
            "Title": article_info["title"],
            "Publication Date": article_info.get("publication_date", ""),
            "DOI": article_info.get("doi", []),
            "OpenAlex_ID": article_info["id"],
            "Cited_works": article_info.get("referenced_works", []),
            "Subjects": [
                {
                    TOPIC: {
                        "Name": topic["display_name"],
                        "Score": topic.get("score", None),
                        "ID": topic.get("id", None),
                    },
                    SUBFIELD: {
                        "Name": (
                            topic["subfield"]["display_name"]
                            if "subfield" in topic
                            else None
                        ),
                        "ID": topic["subfield"]["id"] if "subfield" in topic else None,
                    },
                    FIELD: {
                        "Name": (
                            topic["field"]["display_name"] if "field" in topic else None
                        ),
                        "ID": topic["field"]["id"] if "field" in topic else None,
                    },
                    DOMAIN: {
                        "Name": (
                            topic["domain"]["display_name"]
                            if "domain" in topic
                            else None
                        ),
                        "ID": topic["domain"]["id"] if "domain" in topic else None,
                    },
                }
                for topic in article_info.get("topics", [])
            ],
        }
        return article_data
    except KeyError as e:
        logger.error(f"Error extracting data: {e}")
        logger.error(format_exc())
        return None


def process_doi(doi) -> tuple:
    """
    Process an article: retrieve OpenAlex data for an article given by its DOI,
    as well as data for the cited articles

    Args:
        doi (str): article identifier

    Returns:
        tuple: error message if any (str), article data (ict)
    """

    article_data = fetch_article(doi)
    if article_data in [ERROR_404, ERROR_OTHER]:
        return article_data, None

    article = reshape_article_data(article_data)
    if article is None:
        return None, None

    # Get data of cited articles
    cited_articles = []
    logger.info(f"Fetching data for {len(article['Cited_works'])} cited articles")
    # Loop over the cited articles to get the data for them too
    for cited_work in article["Cited_works"]:
        cited_article_data = fetch_article(cited_work)
        if cited_article_data:
            if cited_article_data in [ERROR_404, ERROR_OTHER]:
                # simply ignore if a cited article was not retrived properly
                pass
            else:
                cited_article = reshape_article_data(cited_article_data)
                if cited_article:
                    # No need to keep the cited artivles of a cited article
                    cited_article.pop("Cited_works")
                cited_articles.append(cited_article)

    # Override sub-document "Cited_articles" with the details for each of them
    article["Cited_articles"] = cited_articles
    return None, article


if __name__ == "__main__":

    # Initialize counters and article data list
    articles_data = []
    error_404_count = 0
    other_error_count = 0
    missing_info_count = 0

    # Fetch DOI list and their URIs
    document_list = fetch_document_list()
    logger.info(f"Retrieved {len(document_list)} DOI and document URI pairs")

    if cfg.OPENALEX_API["use_mailto"]:
        # Parallel execution with ThreadPoolExecutor
        logger.info(f"Running with {cfg.OPENALEX_API['max_workers']} workers")
        with ThreadPoolExecutor(
            max_workers=cfg.OPENALEX_API["max_workers"]
        ) as executor:
            future_to_doi = {
                executor.submit(process_doi, item["doi"]): (
                    cfg.DOCUMENT_URI_TEMPLATE % item["paper_id"],
                    item["doi"],
                )
                for item in document_list
            }
            for future in tqdm(as_completed(future_to_doi), total=len(document_list)):
                document_uri, doi = future_to_doi[future]
                try:
                    error, article_data = future.result()
                    if error == ERROR_404:
                        error_404_count += 1
                    elif error == ERROR_OTHER:
                        other_error_count += 1
                    elif article_data:
                        article_data["ISSA_Document_URI"] = document_uri
                        # Ajoute l'URI du document à l'article
                        if (
                            not article_data["Cited_articles"]
                            or not article_data["Subjects"]
                        ):
                            missing_info_count += 1
                        else:
                            articles_data.append(article_data)
                            logger.info(
                                f"Data for DOI {doi} recorded with URI {document_uri}."
                            )
                except Exception as exc:
                    logger.error(f"Exception while processing DOI {doi} : {exc}")
    else:
        # Sequential execution
        logger.info("Running in sequential execution mode")
        for item in tqdm(document_list):
            doi, paper_id = item["doi"], item["paper_id"]
            document_uri = cfg.DOCUMENT_URI_TEMPLATE % paper_id
            error, article_data = process_doi(doi)
            if article_data:
                if error == ERROR_404:
                    error_404_count += 1
                elif error == ERROR_OTHER:
                    other_error_count += 1
                elif article_data:
                    article_data["ISSA_Document_URI"] = document_uri
                    # Ajoute l'URI du document à l'article
                    if (
                        not article_data["Cited_articles"]
                        or not article_data["Subjects"]
                    ):
                        missing_info_count += 1
                    else:
                        articles_data.append(article_data)
                        logger.info(
                            f"Data for DOI {doi} recorded with URI {document_uri}."
                        )

    # Save results to JSON file
    output = cfg.OUTPUT_FILES["article_citation"]
    with open(output, "w", encoding="utf-8") as output_file:
        json.dump(articles_data, output_file, ensure_ascii=False, indent=4)

    # Log summary information
    logger.info(f"Data saved in {output}")
    logger.info(f"Number of articles recorded: {len(articles_data)}")
    logger.info(f"Number of 404 errors: {error_404_count}")
    logger.info(f"Number of other errors: {other_error_count}")
    logger.info(f"Number of articles with missing info: {missing_info_count}")

close_timestamp_logger(logger)
