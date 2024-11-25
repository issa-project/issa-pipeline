# ISSA Processing Pipeline
 
This repository contains the pipeline developed by the [ISSA](https://issa.cirad.fr/) project.
It orchestrates the automatic indexing of a scientific archive by extracting from the articles full-text thematic descriptors and named entities, and linking them with terminological resources in the Semantic Web format.

The repository consists of various tools, scripts and configuration files involved in each step of the pipeline:
- retrieve the articles metadata from the archive's API;
- download and pre-process the PDF files of the articles;
- process the output to extract thematic descriptors and named  entities;
- translate the output of each processing step into a unified, consistent RDF dataset;
- retrieve additional metadata from OpenAlex: topics, Sustainable Devlopment Goals (SDG), authorship with institutions
- upload the resulting dataset to a triple store equipped with a SPARQL endpoint.

These steps are summurized in the following diagram.

<img src="doc/pipeline_diagram.png" width="700" />


## Content

- [Processing pipeline](pipeline/)
- [Extending the pipeline](doc/HOW-TO-EXTEND-PIPELINE.md)
- [Tools related to Docker containers and third-party datasets](environment/)
- [RDF modeling](doc/data-modeling.md)
- [RDF examples](doc/examples/)
- [Vocabulary definitions and RDF dataset description](dataset/)


## License

See the [LICENSE file](LICENSE).


## Cite this work

Toulet, Anne, Franck Michel, Anna Bobasheva, Aline Menin, Sébastien Dupré, Marie-Claude Deboin, Marco Winckler, and Andon Tchechmedjiev. "ISSA: generic pipeline, knowledge model and visualization tools to help scientists search and make sense of a scientific archive." In The Semantic Web–ISWC 2022: 21st International Semantic Web Conference, Virtual Event, October 23–27, 2022, Proceedings, pp. 660-677. Cham: Springer International Publishing, 2022. https://doi.org/10.1007/978-3-031-19433-7_38 
<details>
<summary>See BibTex</summary>

@inproceedings{toulet2022issa,
  title={ISSA: generic pipeline, knowledge model and visualization tools to help scientists search and make sense of a scientific archive},
  author={Toulet, Anne and Michel, Franck and Bobasheva, Anna and Menin, Aline and Dupr{\'e}, S{\'e}bastien and Deboin, Marie-Claude and Winckler, Marco and Tchechmedjiev, Andon},
  booktitle={The Semantic Web--ISWC 2022: 21st International Semantic Web Conference, Virtual Event, October 23--27, 2022, Proceedings},
  pages={660--677},
  year={2022},
  organization={Springer}
}
</details>


Anna BOBASHEVA, Franck MICHEL, Andon TCHECHMEDJIEV, Anne TOULET (2022). ISSA Processing Pipeline. https://github.com/issa-project/issa-pipeline.

<details>
<summary>See BibTex</summary>

@software{BOBASHEVA_issa-pipeline_2022,
author = {BOBASHEVA, Anna and MICHEL, Franck and TCHECHMEDJIEV, Andon and TOULET, Anne},
doi = {10.5281/zenodo.6513983},
month = {5},
title = {{issa-pipeline}},
url = {https://github.com/issa-project/issa-pipeline},
version = {1.0.0},
year = {2022}
}
</details>
