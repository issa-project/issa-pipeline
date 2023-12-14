#!/usr/bin/env python
# coding: utf-8

# Translating MeSH labels into French
# Manually download *fredesc2022.xml* with MeSH concepts in English and French
# from https://mesh.inserm.fr/FrenchMesh/
# 
# Assuming *mesh-en.tsv* was created by pyclinrec Docker already

import xml.etree.ElementTree as ET
import pandas as pd
import os

# Read App cache dir from environment variable
APP_CACHE_DIR = os.environ.get('PYCLINREC_HOST_CACHE') or ''
MESH_FR_XML = 'fredesc2022.xml'
INPUT_MESH_FILE = os.path.join(APP_CACHE_DIR, 'mesh-en.tsv')
OUTPUT_MESH_FILE = os.path.join(APP_CACHE_DIR, 'mesh-fr.tsv')

def parse_mesh_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    mesh_dict = {}

    for dn in root.findall('*/DescriptorName'):
        en = dn.find('StringUS').text
        fr = dn.find('StringFR').text
        mesh_dict[en] = fr

    for dn in root.findall('.//QualifierName'):
        en = dn.find('StringUS').text
        fr = dn.find('StringFR').text
        mesh_dict[en] = fr

    return mesh_dict

def translate_mesh_labels(mesh_dict, input_file, output_file):
    mesh_en = pd.read_csv(input_file, sep='\t', header=None, names=['uri', 'en'])

    # Translate
    mesh_en['fr'] = mesh_en['en'].map(mesh_dict.get)

    translated_mesh = mesh_en[mesh_en['fr'].notnull()]
    translated_mesh.to_csv(output_file, sep='\t', columns=['uri', 'fr'],
                           index=False, header=False,
                           encoding='utf-8', line_terminator='\n')

if __name__ == "__main__":
    mesh_dict = parse_mesh_xml(MESH_FR_XML)
    print(f"Number of English-French translations: {len(mesh_dict)}")

    translate_mesh_labels(mesh_dict, INPUT_MESH_FILE, OUTPUT_MESH_FILE)
    print(f"Translations saved to {OUTPUT_MESH_FILE}")
