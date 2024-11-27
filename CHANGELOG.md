# ISSA Pipeline Changelog

## [2.1.0] 2024-11-27

A new step was added to the pipeline to perform 2 major actions:
- retrieve complementary metadata about the documents from OpenAlex: topics, Sustainable Devlopment Goals (SDG), authorship with institutions
- compute, for each document, the Rao Stirling diversity index, using citation and topics data retrieved from OpenAlex

## [2.0.0] 2023-12-14

Enhanced and refactored ISSA pipeline into a new version that supports easily configurable multi-instance pipelines.

- Upgraded ISSA pipeline environment
   - upgraded the execution environment with available upgrades of the tools:  Grobid, Entity-Fishing, Pyclinrec
   - added Morph-xR2RML Dockers instead of MongoDB and host-based morph-xr2rml java application
- Extended Agritrop KG 
   - annotate documents beyond articles, e.g. theses, conference papers, etc. without full-text extraction
   - added document domain descriptors
- Refactored the code to support multi-instance deployment
  - with a minimal effort to launch a new ISSA pipeline for another document corpus
  - and the support for running multiple pipelines and SPARQL endpoints on the same machine
- Added the configuration for the HAL EuroMov ISSA pipeline
