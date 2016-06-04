#!/usr/bin/python3

from xml.etree import cElementTree

class BiggestTownsVisualiser(object):
    stat_filepath = None
    obec_filepath = None

    def __init__(self, stat_filepath, obec_filepath):
        self.stat_filepath = stat_filepath
        self.obec_filepath = obec_filepath

    def find(self):
        tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
        tree_obec = cElementTree.ElementTree(file=self.obec_filepath)
        root = tree_stat.getroot()
        kraje = root.findall(".//Kraj")
        maxValues = [None]*len(kraje)
        i = 0
        for kraj in kraje:
            maximum = [0,None,None,kraj.find("Nazev").text]
            for okres in root.iter('Okres'):
                if okres.get("kod")[0:2] == kraj.get("kod"):
                    for obec in root.iter('Obec'):
                        if obec.get("okres") == okres.get("kod"):
                            for obec_ulice in tree_obec.getroot().iter('AdresniMista'):
                                if obec_ulice.get("obec") == obec.get("kod"):
                                    pocetAdresnichMist = int(obec_ulice.find("pocetAdresnichMist").text)
                                    if pocetAdresnichMist > maximum[0]:
                                        maximum = [pocetAdresnichMist, obec.get("kod"), obec.find("Nazev").text, kraj.find("Nazev").text]
            maxValues[i] = maximum
            i = i + 1
        return maxValues

"""
if __name__ == '__main__':
    visualiser = BiggestTownsVisualiser("sample_stat.xml","sample_obecbezulic.xml")
    values = visualiser.find()
    print(values)
"""
