#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_areas
from xml.etree import cElementTree

class SquareCountVisualiser(Visualiser):
	def find(self):
		tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
		tree_ulice = cElementTree.ElementTree(file=self.db_filepath)
		root = tree_stat.getroot()
		okresy = root.findall(".//Okres")
		values=[None]*len(okresy)
		i = 0
		for okres in okresy:
			count=[0,okres.get("kod"), okres.find("Nazev").text]
			for obec in root.iter('Obec'):
				if obec.get("okres") == okres.get("kod"):
					for ulice in tree_ulice.iter('Ulice'):
						if ulice.get("obec") == obec.get("kod"):
							nazev = ulice.find("Nazev").text
							if "nám" in nazev or "Nám" in nazev:
								count = [count[0]+1, okres.get("kod"), okres.find("Nazev").text]
			values[i] = count
			i = i + 1
		return values

	def run(self):
		data = self.find()
		return feature_collection_from_areas(data, self.db_filepath, self.db_filepath, 'Square count in area')
