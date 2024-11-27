# ISSA Pipeline Changelog

## [2.1.0] 2024-11-27

### Added

A new step was added to the pipeline to perform 2 major actions:
- retrieve complementary metadata about the documents from OpenAlex: topics, Sustainable Devlopment Goals (SDG), authorship with institutions
- compute, for each document, the Rao Stirling diversity index, using citation and topics data retrieved from OpenAlex
