import os.path
import os
import re

#Nettoyage d'une ligne
def Clean(l) :
    #Remplace les espaces entre les balises par un saut de ligne, puis les espaces
    l = re.sub("\>( *)\<", r">\n\1<", l)
    #Retire les alternanteName, officialName et shortName  hors fr et en
    l = re.sub("\<gn:(alternateName|officialName|shortName) xml:lang=\"(?!fr|en).*\"\>.*\</gn:(alternateName|officialName|shortName)\>", "", l)
    #Retire les lignes vides
    l = re.sub("\n\s*\n", "\n", l, flags=re.MULTILINE)
        #Retine balise rdf fermante
    l = re.sub("\</rdf:RDF\>", "", l)
    return l

with open("all-geonames-rdf.txt", "r", encoding='utf-8') as r :
    with open("all-geonames-rdf.xml", "w", True, encoding='utf-8') as w :
        
        #Première ligne ignorée
        r.readline()

        #Deuxième ligne
        l = r.readline()
        l = Clean(l)
        w.write(l)

        passe = True
        #Reste du fichier
        for line in r:
            
            #Saute une ligne sur 2 (les urls)
            if(not passe):
                #On retire la balise xml
                line = re.sub("\<\?xml version=\"1\.0\" encoding=\"UTF-8\" standalone=\"no\"\?\>\<rdf\:RDF xmlns\:cc=\"http\://creativecommons\.org/ns#\" xmlns\:dcterms=\"http\://purl\.org/dc/terms/\" xmlns\:foaf=\"http\://xmlns\.com/foaf/0\.1/\" xmlns\:gn=\"http\://www\.geonames\.org/ontology#\" xmlns\:owl=\"http\://www\.w3\.org/2002/07/owl#\" xmlns\:rdf=\"http\://www\.w3\.org/1999/02/22-rdf-syntax-ns#\" xmlns\:rdfs=\"http\://www\.w3\.org/2000/01/rdf-schema#\" xmlns\:wgs84_pos=\"http\://www\.w3\.org/2003/01/geo/wgs84_pos#\"\>", "", line)
                line = Clean(line)
                w.write(line)

            passe = not passe
        
        w.write("</rdf:RDF>")
