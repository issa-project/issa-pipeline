## Initialize piclinrec annoatators
import os
import json 
from ConceptAnnotator import ConceptDictionaryGenerator, ConceptAnnotatorCached

APP_CACHE =      os.environ.get("APP_CACHE", default='.')
DICT_ENDPOINT  = os.environ.get('DICT_ENDPOINT' , default='https://data-issa.cirad.fr/sparql')
DICT_GRAPH  =    os.environ.get('DICT_GRAPH' , default='http://agrovoc.fao.org/graph')

dictionaries = {}
for lang in ['en', 'fr']:
    dictionaries[lang] = ConceptDictionaryGenerator(language=lang,
                                                    endpoint=DICT_ENDPOINT,
                                                    graph=DICT_GRAPH,
                                                    output_dir=APP_CACHE).output
    print(f'dictionary file is ready: {dictionaries[lang]}')

annotators = {}
for lang in ['en', 'fr']:
    annotators[lang] = ConceptAnnotatorCached(dictionary_file=dictionaries[lang], 
                                        language=lang, cache_dir=APP_CACHE)
    print(f'annotator is ready:  {len(annotators[lang].concept_recognizer.concept_index)} {lang} concepts')                                    

## Initialose Web App 

from flask import Flask
from flask import request

app = Flask('Agrovoc Annotation WebServer')

## Web App requests

@app.route('/')
def get_data():
    return """Welcome to text annottaion application. <br>
    To submit a text for annotation use POST request http://localhost:5000/annotate with parameters:<br>
    <ul>
    <li><strong>text</strong> - text to annotate</li>
    <li><strong>lang</strong> - one of 'en' or'fr'</li>
    <li><strong>conf</strong> - min confidence score in (0.0 - 1.0) interval</li> 
    </ul>
    <br>
    Response will be in JSON format:<br>
    { "text": &lttext&gt, <br>,
      "concepts" : &ltlist of concepts&gt}}
    """

# Simple get for verification purposes only
@app.route('/annotate_text/<lang>/<text>/')
def annotate_get(text, lang):
    annottaions = annotators[lang].annotate_text(text)
    return json.dumps( {'text':  text,
                            'concepts' : annottaions})
    #return annotators[lang].annotate_text(text)

# Post request for long text
@app.route('/annotate' , methods = ['POST'])
def annotate_post():
    if request.method == 'POST':
        text = request.form.get('text') or ''
        lang = request.form.get('lang') or 'en'
        conf = float(request.form.get('conf') or '0.0')
        
        annottaions = annotators[lang].annotate_text(text, conf_score=conf)
        return json.dumps( {'text':  text,
                            'concepts' : annottaions})
    




