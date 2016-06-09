#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_streets
from xml.etree import cElementTree

class ExtremeStreetNamesVisualiser(Visualiser):
	def find(self):
		tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
		tree_ulice = cElementTree.ElementTree(file=self.db_filepath)
		root = tree_stat.getroot()
		kraje = root.findall(".//Kraj")
		max_values = [None]*len(kraje)
		min_values = [None]*len(kraje)
		i = 0
		for kraj in kraje:
			minimum = (257, None, None, None, None)
			maximum = [-1, None, None, None, None]
			for okres in root.iter('Okres'):
				if okres.get("kod")[0:2] == kraj.get("kod"):
					for obec in root.iter('Obec'):
						if obec.get("okres") == okres.get("kod"):
							for ulice in tree_ulice.getroot().iter('Ulice'):
								if ulice.get("obec") == obec.get("kod"):
									nazev = ulice.find("Nazev").text
									if minimum[0] > len(nazev):
										minimum = (len(nazev), ulice.get("kod"), ulice.find("Nazev").text, obec.find("Nazev").text, kraj.find("Nazev").text)
									if maximum[0] < len(nazev):
										maximum = (len(nazev), ulice.get("kod"), ulice.find("Nazev").text, obec.find("Nazev").text, kraj.find("Nazev").text)
			min_values[i] = minimum
			max_values[i] = maximum
			i = i + 1
		return min_values, max_values

	def run(self):
		(minimal_names, maximal_names) = self.find()

		return feature_collection_from_streets(minimal_names + maximal_names, self.db_filepath, 'Extreme street names in region')
