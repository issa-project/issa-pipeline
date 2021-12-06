# Generation of the Named Entity files used for the ISSA dataset
**WARNINGS:** 
- **The progress bar is broken in this version, it just gives an idea of when a task is finished.**
- **We rely on the [pycld2 package](https://github.com/aboSamoor/pycld2) for language detection which currently excludes Windows support.**
- These scripts need refactoring

****

Script `run_ner.sh` is an entrypoint script. 

The scripts depend on the docker containers for *dbpedia-spotlight.en*, *dbpedia-spotlight.fr*, and *entity-fishing* 

TODO: document the docker containers

