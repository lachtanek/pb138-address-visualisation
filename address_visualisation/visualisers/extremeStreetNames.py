#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_streets
import geojson
from xml.etree import cElementTree

class ExtremeStreetNamesVisualiser(Visualiser):
    def find(self):
        tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
        tree_ulice = cElementTree.ElementTree(file=self.db_filepath)
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

    def run(self, output_directory):
        (minimal_names, maximal_names) = self.find()

        min_f = open(output_directory + '/' + 'minimal_names.json', 'w')
        min_f.write(geojson.dumps(feature_collection_from_streets(minimal_names, self.db_filepath, 'Minimal street names in region')))
        max_f = open(output_directory + '/' + 'maximal_names.json', 'w')
        min_f.write(geojson.dumps(feature_collection_from_streets(maximal_names, self.db_filepath, 'Maximal street names in region')))
