
# Training Thematic Indexing Models

To automate the thematic indexing of the documents we use a tool developed by the National Library of Finland called [Annif](https://annif.org/).

Annif is an easy-to-use dockerized package. It includes a combination of existing natural language processing and machine learning tools including TensorFlow, Omikuji, fastText and Gensim. It is multilingual and can support any subject vocabulary in SKOS or TSV format. Full [documentation](https://github.com/NatLibFi/Annif/wiki)  and extensive  [tutorials](https://github.com/NatLibFi/Annif-tutorial) are provided by its developers.

Preparing an Annif model to be integrated into the ISSA pipeline for automated indexing requires the following steps (done only once):

- install Annif docker container
- configure the projects (models)
- prepare the corpus from existing indexed data
- prepare the vocabularies
- train and evaluate models
- choose the best model

This process is semi-automatic.

## Install Annif docker container

Annif Docker image installation instructions can be found [here](../environment/containers#annif).

## Configure the Annif projects

For the Agritrop use case, we did some preliminary studies and as a result we created a required [project.cfg](./projects.cfg) file to configure the models that we want to try. The config includes models:

- [TFIDF](https://github.com/NatLibFi/Annif/wiki/Backend%3A-TF-IDF) - term frequency model (baseline)
- [Omikuji Parabel](https://github.com/NatLibFi/Annif/wiki/Backend%3A-Omikuji) - tree-based associative machine learning model
- [MLLM](https://github.com/NatLibFi/Annif/wiki/Backend%3A-MLLM)  - lexical algorithm
- [ensemble](https://github.com/NatLibFi/Annif/wiki/Backend%3A-Ensemble) of Omikuji Parabel and MLLM models - combines results from the projects
- [neural network ensemble](https://github.com/NatLibFi/Annif/wiki/Backend%3A-nn_ensemble) of Omikuji Parabel and MLLM models - combines results from the projects and trains NN on these results

Notice that each model relies on a language version of a vocabulary. In the use case of Agritrop the languages are French and English.

## Prepare the corpus

This step assumes that the initial batch of documents is downloaded and the text is extracted and stored in JSON format (the first two steps of the ISSA pipeline).

Run [run-generate-training-dataset.sh](./run-generate-training-dataset.sh) to generate train and test sets.

In the directory specified by `ANNIF_TRAINING_DIR` in the [env.sh](../config/agritrop/env.sh) this script creates a separate subdirectory for each language containing the TXT files with text and TSV files with labels.

The size of the training corpus, train/test split ratio, and other parameters can be configured in [config.py](../config/agritrop/config.py).

## Prepare the vocabularies

A subject vocabulary for the Agritrop use case is [Agrrovoc Thesaurus](https://data.apps.fao.org/catalog/organization/about/agrovoc).

Run [run-generate-vocabulary.sh](./run-generate-vocabularies.sh) to create language specific SKOS vocabularies that can be used by Annif.

The vocabulary files are placed in the same directory as the generated datasets described above.

## Train and evaluate models

Run [run-annif-training.sh](./run-annif-training.sh) to train configured Annif models.

This script launches the scripts [train-and-evaluate_en.sh](./train-and-evaluate_en.sh) and [train-and-evaluate_fr.sh](./train-and-evaluate_fr.sh) in the context of the Annif Docker container. These scripts train the models defined in [project.cfg](./projects.cfg) and evaluate their performance on test data.

## Choose the best model

The output of the training and evaluation is logged in the log files that are stored in the _logs_ subdirectory.

To choose the best model we looked at the log files for the model which gives the best quality metrics. We've chosen to use the document average F1 score to evaluate the top 10 (eval command default) term suggestions by the models against the terms identified by human documentalists.

For Agritrop use case the following scores were evaluated and the _ensemble NN Parabel+MLLM_ model was selected for the pipeline indexing.

English:
| Model:           | TF-IDF |Omikuji Parabel| MLLM | ens Parabel+MLLM | ens NN Parabel+MLLM
|:---------------- |:-------|:--------------|:-----|:-----------------|:-----------------|
| F1@10 (doc. avg) | 0.24   | 0.33          | 0.33 | 0.37             | 0.38             |

French:
| Model:           | TF-IDF |Omikuji Parabel| MLLM | ens Parabel+MLLM | ens NN Parabel+MLLM
|:---------------- |:-------|:--------------|:-----|:-----------------|:-----------------|
| F1@10 (doc. avg) | 0.22   | 0.40          | 0.36 | 0.39             | 0.42             |


After choosing the indexing model the variables in [env.sh](../config/agritrop/env.sh) are set to be used by the pipeline, e.g.:

```bash
ANNIF_PROJECT=cirad-nn-ensemble            # name of the best model minus language suffix
export ANNIF_SUFFIX=.parabel_mllm_nn.tsv   # suffix to add to the indexing output file 
ANNIF_LIMIT=15                             # max number of returned descriptors
ANNIF_THRESHOLD=0.1                        # confidence threshold of returned descriptors
```
