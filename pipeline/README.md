# ISSA Pipeline

ISSA pipeline consists of steps that flow documents from obtaining their metadata trough the processed of text extraction and annotations to the publication aa a Knowledge Graph.

{image here}

To adapt this pipeline to a differnt document repository only the downloadin metadata step has to be modified.

## Source Code

ISSA pipeline's source code is a cmbination of Python scripts for data processing and bash scripts for data flow. 

## Configuration

There are two levels of configuration that pre-define the dataflow and processing options:
 - environnment and data loaction is defined in [env.sh](https://github.com/issa-project/issa-pipeline/blob/main/env.sh)
 - processing configuration for Python scripts is defined in [config.py](https://github.com/issa-project/issa-pipeline/blob/main/pipeline/config.py)
