## Initialize pyclinrec annotators
import os
import json 
from ConceptAnnotator import ConceptDictionaryGenerator, ConceptAnnotatorCached

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


APP_CACHE =      os.environ.get("APP_CACHE", default='/app/cache')
#DICT_ENDPOINT  = os.environ.get('DICT_ENDPOINT' , 'https://data-issa.cirad.fr/sparql')
#DICT_GRAPH  =    os.environ.get('DICT_GRAPH' , default='http://dist.cirad.fr/agrist-thema/graph') 
#DICT_NAME =      os.environ.get('DICT_NAME' , default='mydict' )

dictionaries = {}
annotators = {}

from flask import Flask
from flask import request

app = Flask('Pycinrec Annotation WebServer')

def _load_annotator(dict_name, 
                    lang, 
                    endpoint='',
                    graph='', 
                    skosXL=False,
                    cache_dir=APP_CACHE ):
    """
    Load annotator from cache or generate it
    """
    global dictionaries
    global annotators

    if f'{dict_name}-{lang}' not in annotators:
        dictionaries[f'{dict_name}-{lang}'] = ConceptDictionaryGenerator(
                                                            name=dict_name,
                                                            language=lang,
                                                            endpoint=endpoint,
                                                            graph=graph,
                                                            skosXL=skosXL,
                                                            output_dir=cache_dir).output
                
        annotators[f'{dict_name}-{lang}'] = ConceptAnnotatorCached(dictionary_file=dictionaries[f'{dict_name}-{lang}'],
                                                                    language=lang, 
                                                                    cache_dir=cache_dir)
        print(f'annotator is ready:  {len(annotators[f"{dict_name}-{lang}"].concept_recognizer.concept_index)} {lang} concepts')

def _verify_annotator(dictionary, lang, cache_dir=APP_CACHE):
    """
    Verify if annotator is ready
    """

    global annotators
    if f'{dictionary}-{lang}' not in annotators:
        if ConceptAnnotatorCached.is_cached(dictionary, lang, cache_dir):
            _load_annotator(dictionary, lang)        
        else:
            # Raise application Exception
            raise Exception(f'annotator is not ready: {dictionary}-{lang}')
            

## Web App requests

@app.route('/')
def get_data():
    return """Welcome to text annotation application. <br>
    To submit a text for annotation use POST request http://localhost:5000/annotate with parameters:<br>
    <ul>
    <li><strong>text</strong> - text to annotate</li>
    <li><strong>dictionary</strong> - one of 'mesh' or 'agrovoc'</li>
    <li><strong>lang</strong> - one of 'en' or'fr'</li>
    <li><strong>conf</strong> - min confidence score in (0.0 - 1.0) interval</li> 
    </ul>
    <br>
    A response will be in JSON format:<br>
    { "text": &lttext&gt, <br>,
      "concepts" : &ltlist of concepts&gt}}
    """

@app.route('/annotate_text/<dictionary>/<lang>/<text>/')
def annotate_get(text, lang, dictionary):
    """
    Annotate text with concepts from a dictionary (GET request)
    Simple get for verification purposes only
    """
    global annotators
    try: 
    
        _verify_annotator(dictionary, lang)
        
        annotations = annotators[f'{dictionary}-{lang}'].annotate_text(text)
        
        return json.dumps( {'text':  text,
                                'concepts' : annotations})
    
    except Exception as e:
            return json.dumps( { 'text':  text,
                                'concepts' : [],
                                'error':  str(e)})  
    
@app.route('/annotate' , methods = ['POST'])
def annotate_post():
    """
    Annotate text with concepts from a dictionary (POST request) for long text
    """
    if request.method == 'POST':
        
        text = request.form.get('text') or ''
        dictionary = request.form.get('dictionary') or ''
        lang = request.form.get('lang') or 'en'
        conf = float(request.form.get('conf') or '0.0')

    try:
        _verify_annotator(dictionary, lang)
        
        annotations = annotators[f'{dictionary}-{lang}'].annotate_text(text, conf_score=conf)
        return json.dumps( {'text':  text,
                            'concepts' : annotations})
    except Exception as e:
            return json.dumps( { 'text':  text,
                                'concepts' : [],
                                'error':  str(e)})  

@app.route('/add_annotator' , methods = ['POST'])
def dictionary_post():
    """
    Add a new dictionary and annotator
    """
    global dictionaries
    global annotators

    if request.method == 'POST':

        if 'name' not in request.form:
            raise Exception('dictionary name is required')
        if 'endpoint' not in request.form:
            raise Exception('endpoint is required')
        
        name = request.form.get('name') 
        endpoint = request.form.get('endpoint') 
        graph = request.form.get('graph') or ''
        lang = request.form.get('lang') or 'en'
        skosXL = request.form.get('skosXL') or False
        
        try: 
            _load_annotator(name, lang, endpoint, graph, skosXL=skosXL, cache_dir=APP_CACHE)

            return json.dumps( {'result':  1,
                                'error' : ''})
        except Exception as e:
            return json.dumps( { 'result': 0,
                                'error':  str(e)})  
    

