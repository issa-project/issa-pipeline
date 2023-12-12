## Pyclinrec Docker Image and Container

We build a Docker image to create the execution environment for the [Python Concept Recognition Library](https://github.com/twktheainur/pyclinrec) and access the functionality through a [Flask web framework](https://flask.palletsprojects.com/en/3.0.x/)  application to imitate the annotation API of other annotation Dockers, e.g. `dbpedia-spotlight` or `entity-fishing`.

>:point_right: we forked the library from its original repository for consistency reasons. The forked repository is located [here](https://github.com/issa-project/pyclinrec). The original repository is located [here](https://github.com/twktheainur/pyclinrec).

### Build the Docker image

To build the image and initialize pyclinrec container invoke [install-pyclinrec.sh](install-pyclinrec.sh) script. in this script the image is built based on the [Dockerfile](Dockerfile).

At this stage the `pyclinrec` library package is installed in the image, spaCy language models are downloaded (that takes some time), and the Flask application is copied to the container.

### Create the Docker container and initialize the annotators

By invoking [run-pyclinrec.sh](run-pyclinrec.sh) create the `pyclinrec` Docker container and initialize the annotators by calling the Web API.

The script creates the container based on the Docker image created in the previous step and runs the container in the background. The container is named `pyclinrec` and the `port 5000` is exposed to the host machine.

The script then calls the Web API to initialize the annotators. The annotators are cached in the `/app/cache` directory on the container.

:point_right: It's important to map the host directory to the `/app/cache` volume to persist large objects that take a long time to create.

:point_right: The SKOS thesaurus has to be in place and its endpoint available at this point to successfully create the concept annotator.

:point_right: The script can be run multiple times to initialize different annotators.


### Pyclinrec Web API

Flask application is located in the [app.py](app.py) file. The application exposes the following endpoints:

- http://localhost:5002/ : This GET request returns a welcome message and instructions on how to use the application.

    Usage example:
    ```bash
    curl http://localhost:5002/
    ```
    Response:
    ```html
    Welcome to the Pyclinrec API! .....
    ```

- http://localhost:5002/add_annotator: This endpoint receives a POST request to create a flat dictionary from a SKOS thesaurus and based on this dictionary creates a [Concept Annotator]() object that is subsequently cached in the `/app/cache` directory on the container. The request body contains parameters:

    - name - the name of the dictionary
    - lang - the language of the dictionary
    - endpoint - the URL of the SPARQL endpoint of the thesaurus
    - graph - (optional, default: no specific named graph) the name of the named graph in the endpoint containing the thesaurus
    - skosXL  - (optional, default: False) a boolean value indicating whether the thesaurus labels represented as [SKOS-XL](https://www.w3.org/TR/skos-reference/skos-xl.html) or [SKOS](https://www.w3.org/TR/skos-reference/)

    The response is a JSON object with the following fields:

    - result - an integer value indicating whether the annotator was created successfully (1) or not (0)
    - error - a string containing an error message if the annotator was not created successfully

    Usage example:
    ```bash
    curl -X POST http://localhost:5002/add_annotator \
    --data-urlencode "name=agrovoc" \
    --data-urlencode "lang=en" \
    --data-urlencode "endpoint=http://data-issa.cirad.fr/sparql" \
    --data-urlencode "graph=http://aims.fao.org/aos/agrovoc" \
    --data-urlencode "skosXL=True" \
    -H "Accept: application/json"
    ```
    Response example:
    ```
    {"result":1,"error":""}
    ```

-  http://localhost:5002/annotate_text/{dictionary}/{lang}/{text} : This GET request receives a dictionary name, a language, and a text as parameters in the URL. It returns the annotated text with concepts from the specified dictionary. This endpoint is used mainly for verification purposes and annotating short text.
    
    Usage example:
    ```
    curl http://localhost:5002/annotate_text/agrovoc/en/Growing%20bananas%20in%20Ireland/
    ```

    Response example:
    ```json
    { "text": "Growing bananas in Ireland", 
      "concepts": [
                  {"concept_id": "http://aims.fao.org/aos/agrovoc/c_3948", "start": 19, "end": 26, "matched_text": "Ireland", "confidence_score": 1}, 
                  {"concept_id": "http://aims.fao.org/aos/agrovoc/c_806", "start": 8, "end": 15, "matched_text": "bananas", "confidence_score": 1}
                  ]
    }
    ```

- http://localhost:5002/annotate: This endpoint receives a POST request with the parameters in the request body listed below. This request is intended for annotating long texts.

     - text - the text to be annotated
    - dictionary - the name of the dictionary to be used for annotation
    - lang - the language of the text
    - conf - (optional, default: 0.15, for future use) the confidence score threshold for the concepts to be returned

It returns the JSON object with the annotated text with concepts from the specified dictionary:

- text - annotated text
- concepts - a list of concepts with the following fields:
    - concept_id - the URI of the concept
    - start - the start position of the matched text in the text
    - end - the end position of the matched text in the text
    - matched_text - the matched text
    - confidence_score - the confidence score of the match

Usage example:
```bash
curl -X POST http://localhost:5002/annotate \
--data-urlencode "text=Cultiver des bananes en Irlande" \
--data-urlencode "dictionary=agrovoc" \
--data-urlencode "lang=fr" \
--data-urlencode "conf=0.15" \
-H "Accept: application/json"
```

Response example:
```json
{
    "text": "Cultiver des bananes en Irlande", 
    "concepts": [
                {"concept_id": "http://aims.fao.org/aos/agrovoc/c_3948", "start": 24, "end": 31, "matched_text": "Irlande", "confidence_score": 1}
                ]
}
``` 

### ConceptAnnotator module

The application uses the [ConceptAnnotator module](ConceptAnnotator.py) to generate concept dictionaries and annotate texts. The dictionaries and annotators are stored in global variables and can be loaded from cache `/app/cache` or generated as needed. See the module documentation for details. 

The basis for the module is the [pyclinrec library example](https://github.com/twktheainur/pyclinrec/tree/master/example_applications/agrovoc)
