# ISSA Execution Environment

To facilitate the execution of the pipeline we built an environment that supports Python scripts and Java application execution and capable of securily servicing HTTP requests. For using the third party tools we havily rely on Docker containers either of-the-shelf or custom built. This provides a stable execution environment that is easy to maintain. Data persistence and interaction between the host machine and containers is enabled using Docker volumes.      

<img src="../doc/environment_diagram.png" width="700" />

Minimal host machine specification:
- 64-bit Linux OS
- CPU 2.30 Gz (multi-core is preferable)
- RAM 32 Gb   

Host Environment components with the vesrion tested:
- Python (3.6.8)
- Java (15.0.2)
- Docker (20.10.5)
- Apache web server (2.4.6)

The pipeline's Python scripts are run in a context of virtual environment. The packages requirements and virtual environment buiding script is included in this repository. 

Off-the-shelf Docker containers:
- Grobid (0.7.0)
- MongoDB (5.0.3)
- Annif (0.55)
- DBPedia Spotlight (latest, no specific version tag is available)
- OpenLink Virtuoso (7.2) 

Each container can be downloaded from the Docker Hub and we provide the examples of install and run commands in this repository.  

Custom built containers:
- Entity-fishing (TBD)

For custom built containers we provide dockerfile file(s).

DBpedia Spotlight and Entity-fishing are installed using pre-trained language models.  In our use case we only use French and English models but this can be easily customised.
 
Optionally and depending on the use case some additional external datasets can be obtained from an origine and uploaded to ISSA triple store for faster data access. In our use case we choose to host periodically updated Agrovoc and GeoNames datasets.  
