## Docker agrovoc-pyclinrec image 
## Hosting Python Concept Recognition Library (pyclinrec) package for text annotation.
## The package is accessed via requests to flask web application that is adapted to Agrocov vocabulary  
## created by Anna Bobasheva for the ISSA project  

## usage example 
## docker build --rm --pull --file Dockerfile -t "agrovoc-pyclinrec:latest" -t "agrovoc-pyclinrec:1.0.0"
## docker run --name agrovoc-pyclinrec --rm -d -p 5000:5000 -v ~/ISSA/volumes/agrovoc-pyclinrec:/app/cache agrovoc-pyclinrec
## where  ~/ISSA/volumes/containers/agrovoc-pyclinrec is a host file system directory for storing the flask application 


# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-bullseye

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Install pyclinrec from the forked repo in ISSA-project
# installs git into the Docker image, as required by tox
RUN apt-get update && apt-get install git -y
RUN python -m pip install git+http://github.com/issa-project/pyclinrec.git
#RUN python -m pip install git+http://github.com/twktheainur/pyclinrec.git

# Download spacy model
RUN python -m spacy download en_core_web_md
RUN python -m spacy download fr_core_news_md

WORKDIR /app
COPY . /app

ENV APP_CACHE=/app/cache
VOLUME /app/cache

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

#CMD ["/bin/bash"]
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
