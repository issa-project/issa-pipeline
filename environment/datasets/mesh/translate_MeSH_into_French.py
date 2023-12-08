#!/usr/bin/env python
# coding: utf-8

# ## Translating MeSH Lables into French
# Downloaded *fredesc2022.xml* with MeSH concepts in english and French
# from https://mesh.inserm.fr/FrenchMesh/
# 
# *mesh-en.tsv* was created by pyclinrec

#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
import pandas as pd

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
    mesh_xml_file = 'fredesc2022.xml'
    input_mesh_file = 'mesh-en.tsv'
    output_mesh_file = 'mesh-fr.tsv'

    mesh_dict = parse_mesh_xml(mesh_xml_file)
    print(f"Number of English-French translations: {len(mesh_dict)}")

    translate_mesh_labels(mesh_dict, input_mesh_file, output_mesh_file)
    print(f"Translations saved to {output_mesh_file}")
