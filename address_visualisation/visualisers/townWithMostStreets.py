#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_towns
from xml.etree import cElementTree

class TownWithMostStreetsVisualiser(Visualiser):
    def find(self):
        tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
        tree_ulice = cElementTree.ElementTree(file=self.db_filepath)
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
                            count = 0
                            for ulice in tree_ulice.getroot().iter('Ulice'):
                                if ulice.get("obec") == obec.get("kod"):
                                    count = count + 1
                            if count > maximum[0]:
                                maximum = [count, obec.get("kod"), obec.find("Nazev").text, kraj.find("Nazev").text]
            maxValues[i] = maximum
            i = i + 1

        return maxValues

    def run(self):
        data = towns_with_most_streets_visualiser.find()
        return feature_collection_from_towns(data, self.db_filepath, 'Towns with most streets in region')
