import json
import requests
from retrying import retry
from math import isnan, isinf

def string2number(value):
    """
    Convert a string to a number
    :param value: string to convert
    :return: integer, float or string
    """
    try:
        return int(value)
    except ValueError:
        try:
            if isnan(float(value)):
                raise ValueError
            if isinf(float(value)):
                raise ValueError
                
            return float(value)
        except ValueError:
            if isinstance(value, list):
                value = str(value)
            return value

class WrapperAnnotator(object):
    def __init__(self, 
                 dbpedia_spotlight_endpoint='https://api.dbpedia-spotlight.org/en/annotate',
                 entity_fishing_endpoint='https://cloud.science-miner.com/nerd//service/disambiguate',
                 ncbo_annotatorplus_enpoint='https://bioportal.bioontology.org/',
                 concept_annotator_endpoint='http://localhost:5000/annotate'):
        
        self.dbpedia_spotlight_endpoint = dbpedia_spotlight_endpoint
        self.entity_fishing_endpoint =    entity_fishing_endpoint
        self.ncbo_annotatorplus_enpoint = ncbo_annotatorplus_enpoint
        self.concept_annotator_endpoint = concept_annotator_endpoint
    
    @retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=2000)
    def request_dbpedia_spotlight(self, text, lang='en', confidence=0.15, support=10, postprocess_callback=None):
        """
        Wrapper around DBpedia Spotlight
        :param text: String, text to be annotated
        :param lang: string, language model to use
        :param confidence: float, confidence score for disambiguation / linking
        :param support: integer, how prominent is this entity in Lucene Model, i.e. number of inlinks in Wikipedia
        :return: annotations in an Json array
        """
        try:
            if not lang:
                lang = 'en'

            endpoint = self.dbpedia_spotlight_endpoint
            
            if isinstance(self.dbpedia_spotlight_endpoint, dict):
                endpoint = self.dbpedia_spotlight_endpoint[lang]
                
            headers = {'accept': 'application/json'}
            params = {
                'text': text,
                'confidence': confidence,
                'support': support,
            }
            
            # not supported by get if text too long
            response = requests.post(endpoint, data=params, headers=headers)
            
            if postprocess_callback:
                return postprocess_callback(json.loads(response.text))
            
            # Default behaviour as it was originaly defined in this code
            result = json.loads(response.text)["Resources"]
            result = [{x.replace('@', ''): string2number(v) for x, v in r.items()} for r in result]
            return result

        # null
        except json.decoder.JSONDecodeError:
            return None
        except KeyError:
            return None

    #@retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=10, wait_random_max=2000)
    def request_entity_fishing(self, text, lang='en', postprocess_callback=None):
        """
        Wrapper around Entity-fishing (language set in English)
        :param text: string, text to be annotated
        :param lang: string, language model to use
        :return: annotations in JSON
        """
        try:
            if not lang:
                lang = 'en'
                
            endpoint = self.entity_fishing_endpoint
            
            if isinstance(self.entity_fishing_endpoint, dict):
                endpoint = self.entity_fishing_endpoint['disambiguation']

            files = {
                'query': (
                          '{ \'text\': ' + json.dumps(text) + ',\'language\':{\'lang\': \'' + lang + '\'}}'),
            }

            response = requests.post(endpoint, files=files)
            
            if postprocess_callback:
                return postprocess_callback(json.loads(response.text))
            
            return json.loads(response.text)

        # null
        except json.decoder.JSONDecodeError:
            return None
        
    def request_entity_fishing_short(self, text, lang='en', postprocess_callback=None):
        """
        Wrapper around Entity-fishing (language set in English)
        :param text: string, text to be annotated
        :param lang: string, language model to use
        :return: annotations in JSON
        """
        try:
            if not lang:
                lang = 'en'
                
            endpoint = self.entity_fishing_endpoint
            
            if isinstance(self.entity_fishing_endpoint, dict):
                endpoint = self.entity_fishing_endpoint['disambiguation']

            files = {
                'query': (
                          '{ \'shortText\': "' + text + '",\'language\':{\'lang\': \'' + lang + '\'}}'),
            }

            response = requests.post(endpoint, files=files)
            
            if postprocess_callback:
                return postprocess_callback(json.loads(response.text))
            
            return json.loads(response.text)

        # null
        except json.decoder.JSONDecodeError:
            return None
    
    def request_entity_fishing_concept_lookup(self, wikidataID, postprocess_callback=None):
        """
        Wrapper around Entity-fishing (language set in English)
        :param text: string, text to be annotated
        :param lang: string, language model to use
        :return: annotations in JSON
        """
        try:
               
            endpoint = self.entity_fishing_endpoint
            
            if isinstance(self.entity_fishing_endpoint, dict):
                endpoint = self.entity_fishing_endpoint['concept_lookup']

            get_url = '%s/%s' % (endpoint , wikidataID)

            response = requests.get(get_url)
            
            if postprocess_callback:
                return postprocess_callback(json.loads(response.text))
            
            return json.loads(response.text)

        # null
        except json.decoder.JSONDecodeError:
            return None

    def request_ncbo_plus(self, text, lang='en', ncbo_api='https://bioportal.bioontology.org/'):
        """
        Wrapper around the API of the Bioportal AnnotatorPlus
        API link: http://data.bioontology.org/documentation
        :param text: String, text to be annotated
        :param ncbo_api: Dict, Contains a list with API key to access the NCBO API Web Service and the endpoint
        :param lang: string, language model to use
        :return: annotations in JSON
        """
        try:
            if lang not in ('en', 'fr'):
                lang = 'en'
            params = {
                'apikey': ncbo_api[lang][0],
                # options for clinical texts
                'negation': 'false',
                'experiencer': 'false',
                'temporality': 'false',
                # tweaks
                'longest_only': 'true',
                # less verbose
                'display_links': 'false',
                'display_context': 'false',
                'text': text,
            }
            # Option not supported in French
            if lang == 'en':
                params["lemmatize"] = 'true'

            response = requests.get(ncbo_api[lang][1], params=params)
            return json.loads(response.text)

        # null
        except json.decoder.JSONDecodeError:
            return None

    @retry(stop_max_delay=10000, stop_max_attempt_number=5, wait_random_min=1000, wait_random_max=2000)
    def request_concept_annotator(self, text, lang='en', confidence=0.15, postprocess_callback=None):
        """
        Wrapper around Pyclinrec Annotator
        :param text: String, text to be annotated
        :param lang: string, language model to use
        :param confidence: float, confidence score for disambiguation / linking
        :return: annotations in an Json array
        """
        try:
            if not lang:
                lang = 'en'

            endpoint = self.concept_annotator_endpoint
            
                
            headers = {'accept': 'application/json'}
            params = {
                'text': text,
                'lang': lang,
                'conf': confidence,
            }
            
            # not supported by get if text too long
            response = requests.post(endpoint, data=params, headers=headers)
            
            if postprocess_callback:
                return postprocess_callback(json.loads(response.text))
            
            return json.loads(response.text)["concepts"]

        # null
        except json.decoder.JSONDecodeError:
            return None
        except KeyError:
            return None

if __name__ == '__main__':
    
    wa = WrapperAnnotator()
    wa.request_entity_fishing('test-test-test', lang='en')