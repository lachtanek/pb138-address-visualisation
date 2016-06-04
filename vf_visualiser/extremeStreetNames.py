#!/usr/bin/python3

from xml.etree import cElementTree

class ExtremeStreetNamesVisualiser(object):
    stat_filepath = None
    obec_filepath = None

    def __init__(self, stat_filepath, ulice_filepath):
        self.stat_filepath = stat_filepath
        self.obec_filepath = ulice_filepath

    def find(self):
        tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
        tree_ulice = cElementTree.ElementTree(file=self.obec_filepath)
        root = tree_stat.getroot()
        kraje = root.findall(".//Kraj")
        maxValues = [None]*len(kraje)
        minValues = [None]*len(kraje)
        i = 0
        for kraj in kraje:
            minimum = [257,None,None,None,None]
            maximum = [-1,None,None,None,None]
            for okres in root.iter('Okres'):
                if okres.get("kod")[0:2] == kraj.get("kod"):
                    for obec in root.iter('Obec'):
                        if obec.get("okres") == okres.get("kod"):
                            for ulice in tree_ulice.getroot().iter('Ulice'):
                                if ulice.get("obec") == obec.get("kod"):
                                    nazev = ulice.find("Nazev").text
                                    if minimum[0] > len(nazev):
                                        minimum = [len(nazev), ulice.get("kod"), ulice.find("Nazev").text, obec.find("Nazev").text, kraj.find("Nazev").text]
                                    if maximum[0] < len(nazev):
                                        maximum = [len(nazev), ulice.get("kod"), ulice.find("Nazev").text, obec.find("Nazev").text, kraj.find("Nazev").text]
            minValues[i] = minimum
            maxValues[i] = maximum
            i = i + 1
        return minValues, maxValues

"""
if __name__ == '__main__':
    visualiser = ExtremeStreetNamesVisualiser("simplified_stat.xml","simplified_obec_kompletni.xml")
    (values1,values2) = visualiser.find()
    print(values1)
    print(values2)
"""

