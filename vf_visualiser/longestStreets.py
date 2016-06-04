#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from xml.etree import cElementTree

class LongestStreetsVisualiser(object):
    stat_filepath = None
    obec_filepath = None
    
    def __init__(self, stat_filepath, ulice_filepath):
        self.stat_filepath = stat_filepath
        self.obec_filepath = ulice_filepath
           
    """
    Produces list of lists:
    [count of address numbers in the street, code of the street, name of the street, name of the town, name of the region]
    one longest street per region
    """      
    def find(self):
        tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
        root = tree_stat.getroot()
        kraje = root.findall(".//Kraj")
        maxValues = [None]*len(kraje)
        i = 0
        for kraj in kraje:
            maximum = [0,None,None,None,kraj.find("Nazev").text]
            for okres in root.iter('Okres'):
                if okres.get("kod")[0:2] == kraj.get("kod"):
                    for obec in root.iter('Obec'):
                        if obec.get("okres") == okres.get("kod"):                            
                            tree_ulice = cElementTree.ElementTree(file=self.obec_filepath)
                            for ulice in tree_ulice.getroot().iter('Ulice'):
                                if ulice.get("obec") == obec.get("kod"):
                                    pocetAdresnichMist = int(ulice.find("PocetAdresnichMist").text)
                                    if pocetAdresnichMist > maximum[0]:
                                        maximum = [pocetAdresnichMist, ulice.get("kod"), ulice.find("Nazev").text, obec.find("Nazev").text, kraj.find("Nazev").text]
                                                
            maxValues[i] = maximum
            i = i + 1
        return maxValues
"""
if __name__ == '__main__':
    visualiser = LongestStreetsVisualiser("simplified_stat.xml","simplified_obec_kompletni.xml")
    values = visualiser.find()
    print(values)
"""    
