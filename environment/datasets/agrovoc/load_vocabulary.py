#!/usr/bin/python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper, TURTLE

import sys
import argparse
  
PARSER = argparse.ArgumentParser(description='Extracting Agrovoc vocabulary for a specified language and adapted for  consumption by Annif')
PARSER.add_argument('--lang',    help='language: eg. en', default="en")
PARSER.add_argument('--output', help='file path for Turtle output' , default="agrovoc_en.ttl")

args = PARSER.parse_args(sys.argv[1:])
print(args)

lang = args.lang
output = args.output

from agrovoc_wrapper import Agrovoc_Wrapper

Agrovoc_Wrapper().download_vocab(lang, output)

