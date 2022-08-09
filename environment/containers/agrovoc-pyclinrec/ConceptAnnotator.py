## 1. generate dictionary file
import os
from pyclinrec.dictionary import generate_dictionary_from_skos_sparql

# default values that are useful for testing 
DICT_NAME = 'agrovoc'
AGROVOC_ENDPOINT = 'http://issa.i3s.unice.fr/sparql'
AGROVOC_GRAPH    = 'http://agrovoc.fao.org/graph'

#AGROVOC_ENDPOINT = 'https://agrovoc.fao.org/sparql'
#AGROVOC_GRAPH    = 'http://aims.fao.org/aos/agrovoc/'


class ConceptDictionaryGenerator:
    def __init__(self,
                 name= DICT_NAME,
                 endpoint = AGROVOC_ENDPOINT,
                 graph    = AGROVOC_GRAPH,
                 language = 'en',
                 output_dir = '.'):
      
      self.endpoint = endpoint
      self.graph = graph
      self.language = language

      self.output = os.path.join(output_dir, f'{name}-{language}.tsv' )

      if not os.path.exists(self.output):
          # generate dict tsv file
          print('generating dictionary..')
          generate_dictionary_from_skos_sparql(endpoint, self.output, 
                                               skos_xl_labels=True, 
                                               lang=language, 
                                               from_statement=graph)

## 2. initialise annotator
import pickle
from pyclinrec.dictionary import MgrepDictionaryLoader
from pyclinrec.recognizer import IntersStemConceptRecognizer
from pyclinrec import __path__ as pyclinrec_path

class ConceptAnnotator:
    def __init__(self, dictionary_file, language='en'):

        dictionary_loader = MgrepDictionaryLoader(dictionary_file)

        self.concept_recognizer = IntersStemConceptRecognizer(dictionary_loader, 
                                                              os.path.join(pyclinrec_path[0], f'stopwords{language}.txt'),
                                                              os.path.join(pyclinrec_path[0], f'termination_terms{language}.txt'))

        self.concept_recognizer.initialize()
 

    def annotate(self, text):
        return self.concept_recognizer.annotate(text)

    def annotate_text(self, text, conf_score=0.0):
        annotations = self.annotate(text)

        attr_list = ['concept_id', 'matched_text', 'confidence_score', 'start', 'end']

        annot_list = []   

        for annot in (annotations[2] or set()):
            if annot.confidence_score > conf_score:
                annot_json = {k: v for k, v in annot.__dict__.items() if k in attr_list}
                annot_list = annot_list + [annot_json]

        return annot_list

class ConceptAnnotatorCached(ConceptAnnotator):
    def __init__(self, dictionary_file, language='en', cache_dir='.'):
        self.cached_file = os.path.join(cache_dir, f'concept-recognizer-{language}.pkl')

        if not os.path.exists(self.cached_file):
            super().__init__(dictionary_file, language)

            # serialize
            with open(self.cached_file, 'wb') as f:
                pickle.dump(self.concept_recognizer, f)
            print( 'concept recogniser serialized')

        else:
            # deserialize
            with open(self.cached_file, 'rb') as f:
                self.concept_recognizer = pickle.load(f)
            print( 'concept recogniser deserialized')

