# -*- coding: utf-8 -*-
""" 
Compute the Rao Stirling index of an article, which measures the diversity of subjects in an article.
It is computed using the subjects assigned, not to the article itself, but to the articles it cites.
See [1]

Here, we use the subjects assigned to articles by Open Alex, which consists of a thesaurus of topics 
grouped into subfields, then fields, then domains at the more genereal level.

The Rao Stirling index relies on the concept of "distance" or "dissimilarity" between two subjects, 
which is a value in [0,1]. This distance will be different depending on the level that we consider for the subject
(topic, subfield, field, domain). This level can be configured in config.py, parameter RAO_STIRLING_CALC_LEVEL.
Below, we use the term 'subject' to refer to one of the levels in the classification of
OpenAlex: topics < subfields < fields < domains.

This script is invoked with one command line argument: the path 
the path to the configuration file containing the class cfg_openalex_data


[1] Loet Leydesdorff, Caroline S. Wagner, Lutz Bornmann. Interdisciplinarity as diversity in citation patterns among journals: Rao-Stirling diversity, relative variety, and the Gini coefficient.
Journal of Informetrics, Volume 13, Issue 1, 2019. https://doi.org/10.1016/j.joi.2018.12.006.

@author: Quentin Scordo, Franck Michel
"""
import csv
from collections import defaultdict
from itertools import combinations
import json
import numpy as np
import os
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


def load_article_data(filepath):
    """
    Load the JSON file previsouly generated and containing article citation data
    """
    logger.info(f"Loading article citation and subjects data from {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def create_article_subjects_citation(article: dict, subject_level: str) -> tuple:
    """
    Calculate, for one article, the proportion of "cited subjects" (topics/subfields/fields/domains)
    based on the occurrence of each subject in the articles cited by this article.
    That is, count the number of times each subject appears in the cited articles,
    and divide by the total number of articles.

    Args:
        article (dict): dictionary containing the citation data of one article
        subject_level (str): the level of the subject of interest, one of vars TOPIC, SUBFIELD, FIELD, DOMAIN

    Returns:
        dict: subject name as a key, and proportion of occurrences
        of this subject in the cited articles as a value
    """

    logger.info(
        f"Calculating the proportion of each {subject_level} in the articles cited by {article['DOI']}"
    )

    subject_count = defaultdict(int)

    no_cited_articles = len(article["Cited_articles"])
    for cited_article in article["Cited_articles"]:
        for subject_subtree in cited_article["Subjects"]:
            subject_name = subject_subtree[subject_level]["Name"]
            subject_count[subject_name] += 1

    logger.info(
        f"Found {len(subject_count)} {subject_level}(s) in {no_cited_articles} cited article(s)"
    )
    article_subjects = {}

    if len(subject_count) > 0:
        for subject, count in subject_count.items():
            article_subjects[subject] = count / no_cited_articles
        logger.debug(f"Proportion of {subject_level}s: {article_subjects}")

    return article_subjects


def create_subjects_citation_matrix(
    articles: dict, subject_list: list, subject_level: str
) -> np.ndarray:
    """
    Generate a matrix containing, for each article, the proportion of subjects in the cited articled,
    + 1 column for the DOI of the article, 1 for its OpenAlex_ID, and 1 for its ISSA document URI

    Args:
        articles (list): full list of articles with citation and subjects data
        subject_list (list): list of all subjects (either topics, subfields, fields or domains) concerned by all the articles
        subject_level (str): the level of the subject of interest, one of vars TOPIC, SUBFIELD, FIELD, DOMAIN

    Returns:
        np.ndarray: a matrix with the 1 line per article, and one column per subject,
        plus 1 column for the DOI and 1 column for the OpenAlex_ID.
        Each cell is the the proportion of this subject in the articles cited by this article.
    """

    logger.info(f"Creating the subject citation matrix at level {subject_level}")

    no_articles = len(articles)
    no_subjects = len(subject_list)
    # no_articles lines X no_topics columns + 2 columns for the DOI and OpenAlex_ID
    subjects_citation_matrix = np.zeros((no_articles, no_subjects + 2), dtype=object)

    for article_index, article in enumerate(articles):
        # First column for DOI, second column for OpenAlex_ID
        subjects_citation_matrix[article_index, 0] = article["DOI"]
        subjects_citation_matrix[article_index, 1] = article["OpenAlex_ID"]
        subjects_citation_matrix[article_index, 2] = article["ISSA_Document_URI"]
        article_subjects_citation = create_article_subjects_citation(
            article, subject_level
        )

        # Fill in the matrix
        for subject_index, subject in enumerate(subject_list):
            # each article may only cite a subset of the subjects, not all of them
            if subject in article_subjects_citation:
                subjects_citation_matrix[article_index, subject_index + 2] = (
                    article_subjects_citation[subject]
                )
            else:
                # If the subject is not cited by this article
                subjects_citation_matrix[article_index, subject_index + 2] = 0

    return subjects_citation_matrix


def precompute_subject_trees(articles: dict, subject_level: str) -> dict:
    """
    Compute a dictionary that associates each subject (may it be a topic, subfield, field or domain)
    of a cited article with the list of topic, subfield, field, and domain that it belongs to.

    Args:
        articles (list): list of articles with citation and subjects data
        subject_level (str): the level of the subject of interest, one of vars TOPIC, SUBFIELD, FIELD, DOMAIN

    Returns:
        dict: dictionary with the subject name as key; the value is a dictionary of its corresponding
        topic, subfield, field, and domain, obtained from a JSON document like the following:
    ```{
            "Topic": {
                "Name": "Emerging Zoonotic Diseases and One Health Approach",
                "Score": 0.9999,
                "ID": "https://openalex.org/T12492"
            },
            "Subfield": {
                "Name": "Public Health, Environmental and Occupational Health",
                "ID": "https://openalex.org/subfields/2739"
            },
            "Field": {
                "Name": "Medicine",
                "ID": "https://openalex.org/fields/27"
            },
            "Domain": {
                "Name": "Health Sciences",
                "ID": "https://openalex.org/domains/4"
            }
        }
    """
    subject_levels = defaultdict(dict)

    for article in articles:
        # for subject_tree in article["Subjects"]:
        #    name = subject_tree[subject_level]["Name"]
        #    subject_levels[name] = subject_tree
        for cited_article in article["Cited_articles"]:
            for subject_tree in cited_article["Subjects"]:
                name = subject_tree[subject_level]["Name"]
                subject_levels[name] = subject_tree

    logger.info(
        f"Precomputed the tree info of {len(subject_levels)} {subject_level}(s)"
    )
    return subject_levels


def calculate_distance(sub_i: dict, sub_j: dict, subject_level: str) -> float:
    """
    Return a distance in [0,1] between two subjects based on their proximity in the OpenAlex tree of subjects.

    Args:
        sub_i (dict): first subject to compare
        sub_j (dict): 2nd subject to compare
        subject_level (str): the level of the subject of interest, one of vars TOPIC, SUBFIELD, FIELD, DOMAIN

    Here, each subject is given by a dictionary with the keys 'Topic', 'Subfield', 'Field', 'Domain',
    obtained from a JSON document like the following:
    ```{
            "Topic": {
                "Name": "Emerging Zoonotic Diseases and One Health Approach",
                "Score": 0.9999,
                "ID": "https://openalex.org/T12492"
            },
            "Subfield": {
                "Name": "Public Health, Environmental and Occupational Health",
                "ID": "https://openalex.org/subfields/2739"
            },
            "Field": {
                "Name": "Medicine",
                "ID": "https://openalex.org/fields/27"
            },
            "Domain": {
                "Name": "Health Sciences",
                "ID": "https://openalex.org/domains/4"
            }
        }

    Returns:
        float: distance in [0,1]
    ```
    """

    distances = {
        # distance between twice the same topic
        TOPIC: 0,
        # distance between 2 different topics in the same subfield
        SUBFIELD: 0.125,
        # distance between 2 topics in different subfields but in the same field
        FIELD: 0.25,
        # distance between 2 topics in different fields but in the same domain
        DOMAIN: 0.5,
        # distance between 2 topics in different domains
        "max": 1,
    }

    if not sub_i or not sub_j:
        return distances["max"]

    if subject_level in (TOPIC) and sub_i[TOPIC]["Name"] == sub_j[TOPIC]["Name"]:
        return distances[TOPIC]

    if (
        subject_level in (TOPIC, SUBFIELD)
        and sub_i[SUBFIELD]["Name"] == sub_j[SUBFIELD]["Name"]
    ):
        return distances[SUBFIELD]

    if (
        subject_level in (TOPIC, SUBFIELD, FIELD)
        and sub_i[FIELD]["Name"] == sub_j[FIELD]["Name"]
    ):
        return distances[FIELD]

    if (
        subject_level in (TOPIC, SUBFIELD, FIELD, DOMAIN)
        and sub_i[DOMAIN]["Name"] == sub_j[DOMAIN]["Name"]
    ):
        return distances[DOMAIN]

    return distances["max"]


def calculate_rao_stirling_index(
    article_subjects_citation: dict, subject_trees: dict, subject_level: str
):
    """
    Calculate the Rao-Stirling index for a single article

    Args:
        article_subjects_citation (dict): dictionary whose key is the subject name, and the value is the proportion of occurrences of this subject in the cited articles
        subject_trees (dict): dictionary whose key is a subject name, and the value is a dictionary of its corresponding topic, subfield, field, and domain
        subject_level (str): the level of the subject of interest, one of vars TOPIC, SUBFIELD, FIELD, DOMAIN

    Returns:
        float: Normalized Rao-Stirling index in [0,1]
    """
    subjects = list(article_subjects_citation.keys())

    sum_rao_stirling = 0.0
    no_combinations = 0

    for sub_i, sub_j in combinations(subjects, 2):
        p_i = article_subjects_citation[sub_i]
        p_j = article_subjects_citation[sub_j]
        d_i_j = calculate_distance(
            subject_trees.get(sub_i), subject_trees.get(sub_j), subject_level
        )
        sum_rao_stirling += p_i * p_j * d_i_j
        no_combinations += 1

    # Normalize the index to have a value in [0,1]
    sum_rao_stirling_idx = sum_rao_stirling / no_combinations
    logger.debug(
        f"Rao Stirling index: {sum_rao_stirling}, normalized by {no_combinations} couples of {subject_level}s: {sum_rao_stirling_idx}"
    )
    return sum_rao_stirling_idx


def calculate_rao_stirling_occurrence_intevals(results, interval_size=0.1) -> dict:
    """
    Sort Rao Stirling index values into intervals

    Args:
        results (list): list of dictionaries with key "Rao Stirling Index"
        interval (float): size of the interval

    Returns:
        dict: dictionary with the interval as key, and the number of occurrences of the Rao Stirling index in this interval as value
    """
    logger.debug(
        f"Sorting Rao Stirling index values into intervals of size {interval_size}"
    )
    occurrences = {}

    # Loop through the ranges to initialize the intervals with value 0
    for i in range(0, int(1 / interval_size)):
        lower_bound = round(i * interval_size, 3)
        upper_bound = round((i + 1) * interval_size, 3)
        if i != int(1 / interval_size):
            occurrences[f"[{lower_bound}-{upper_bound}["] = 0
        else:
            # last interval includes the upper bound 1.0
            occurrences[f"[{lower_bound}-{upper_bound}]"] = 0

    for result in results:
        rao_index = result["Rao_Stirling_Index"]
        for i in range(0, int(1 / interval_size)):
            lower_bound = round(i * interval_size, 3)
            upper_bound = round((i + 1) * interval_size, 3)
            if i != int(1 / interval_size):
                if lower_bound <= rao_index < upper_bound:
                    occurrences[f"[{lower_bound}-{upper_bound}["] += 1
                    break
            else:
                # last interval includes the upper bound 1.0
                if lower_bound <= rao_index <= upper_bound:
                    occurrences[f"[{lower_bound}-{upper_bound}]"] += 1
                    break

    return occurrences


def convert_rao_stirling_value_to_inteval(rao_index: float, interval_size=0.1) -> str:
    """
    Takes a Rao Stirling index value and turns it into an interval as a string
    like "[0.0-0.1[", "[0.1-0.2[" etc.

    Args:
        results (list): list of dictionaries with key "Rao Stirling Index"
        interval (float): size of the interval

    Returns:
        str: interval string representation
    """

    interval = ""
    precision = len(str(int(1 / interval_size) - 1))
    _format = '{:.' + str(precision) + 'f}'

    for i in range(0, int(1 / interval_size)):
        lower_bound = round(i * interval_size, 3)
        upper_bound = round((i + 1) * interval_size, 3)
        if i != int(1 / interval_size):
            if lower_bound <= rao_index < upper_bound:
                interval = f"[{_format.format(lower_bound)}-{_format.format(upper_bound)}["
                break
        else:
            # last interval includes the upper bound 1.0
            if lower_bound <= rao_index <= upper_bound:
                interval = f"[{_format.format(lower_bound)}-{_format.format(upper_bound)}]"
                break

    return interval


def save_citation_matrix_with_topics(matrix, header_row, filepath):
    """
    Save a citation matrix with topics to a CSV file
    """
    logger.info(f"Saving citation matrix to {filepath}")
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(header_row)
        writer.writerows(matrix)


def main():
    """
    Main function to calculate the Rao-Stirling index for all the articles
    """

    level = cfg.RAO_STIRLING_CALC_LEVEL
    logger.info(f"Starting Rao-Stirling calculation at level: {level}")

    articles = load_article_data(cfg.OUTPUT_FILES["article_citation"])
    logger.info(f"Loaded data about {len(articles)} documents")

    rao_stirling_results = []
    missing_info_count = 0
    all_subjects = set()  # To keep track of all the subjects of all the articles

    subject_trees = precompute_subject_trees(articles, level)

    for article in articles:
        if not article["Cited_articles"]:
            missing_info_count += 1
            logger.info(f"No cited articles for {article['DOI']}")
            continue

        # Compute the proportions of citation of each subject for this article
        article_subjects_citation = create_article_subjects_citation(article, level)
        cited_subjects = article_subjects_citation.keys()

        if len(cited_subjects) == 0:
            missing_info_count += 1
            logger.info(f"No cited topics for {article['DOI']}")
            continue

        # Update the set of subjects for all the articles
        all_subjects.update(cited_subjects)

        rao_stirling_index = calculate_rao_stirling_index(
            article_subjects_citation, subject_trees, level
        )
        rao_stirling_results.append(
            {
                "DOI": article["DOI"],
                "ISSA_Document_URI": article["ISSA_Document_URI"],
                "OpenAlex_ID": article["OpenAlex_ID"],
                "Title": article["Title"],
                "Rao_Stirling_Index": rao_stirling_index,
                "Rao_Stirling_Interval": convert_rao_stirling_value_to_inteval(rao_stirling_index),
            }
        )

    all_subjects_list = list(all_subjects)
    if cfg.SAVE_SUBJECT_CITATION_MATRIX:
        # Then create the matrix of all subjects cited in all articles
        subjects_citation_matrix = create_subjects_citation_matrix(
            articles, all_subjects_list, level
        )

        header_row = ["DOI", "OpenAlex_ID", "ISSA_Document_URI"] + all_subjects_list
        matrix_file = cfg.OUTPUT_FILES["subject_citation_matrix"].replace(
            "subject", level
        )
        save_citation_matrix_with_topics(
            subjects_citation_matrix, header_row, matrix_file
        )

    result_file = cfg.OUTPUT_FILES["rao_stirling_index"].replace("subject", level)
    logger.info(f"Saving Rao-Stirling index results to {result_file}")
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(rao_stirling_results, f, ensure_ascii=False, indent=4)

    logger.info(f"Number of articles with missing info: {missing_info_count}")

    # Calc. intervals of occurrence of the Rao-Stirling index
    rao_stirling_index_intervals = calculate_rao_stirling_occurrence_intevals(
        rao_stirling_results, cfg.RAO_STIRLING_INTERVAL
    )
    result_file = cfg.OUTPUT_FILES["rao_stirling_index_intervals"].replace(
        "subject", level
    )
    logger.info(f"Saving Rao-Stirling intervals to {result_file}")
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(rao_stirling_index_intervals, f, ensure_ascii=False, indent=4)

    # Trigger RDF Conversion
    # if config.get("run_rdf_conversion", False):
    #     logger.info("Running RDF conversion script")
    #     os.system("python Interdisciplinarity/rao_stirling_to_rdf.py")


if __name__ == "__main__":
    main()

close_timestamp_logger(logger)
