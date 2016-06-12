#!/usr/bin/python3
"""
Module with visualiser of streets with extreme names in database.
"""

from sys import maxsize
from address_visualisation import Visualiser
from address_visualisation.transform_to_feature_collection import feature_collection_from_streets

class ExtremeStreetNamesVisualiser(Visualiser):
	"""
	Visualiser which finds shortest/longest street names in database xml and turns information about them into geojson format.

	...
	Methods
	-------
	find()
		Finds places with extreme names and returns information about it in 2 arrays of arrays.
	run()
		Calls find method and turns its result to geojson FeatureCollection.
	"""
	def find(self):
		"""
		Finds extreme (shortest and longest) street name in each region in xml tree and returns information about its location.

		For each region, it searches through xml tree for streets in region and checks their names.
		If their name is shorter than minimum or longer than maximum of region,
		method saves information about it into `min_values`/`max_values` on the position of region.

		Returns
		-------
		type
			tuple of lists of lists
		min_values : list of lists
			For each region one array with following information about street with shortest name in region:
			[length of name, code of street, name of street, name of town, name of region]
		max_values : list of lists
			For each region one array with following information about street with longest name in region:
			[length of name, code of street, name of street, name of town, name of region]

		"""
		root = self.db_tree.getroot()

		kraje = root.findall(".//Kraj")
		max_values = {kraj.get("kod"): (0, None, None, None, kraj.find("Nazev").text) for kraj in kraje}
		min_values = {kraj.get("kod"): (maxsize, None, None, None, kraj.find("Nazev").text) for kraj in kraje}

		obce_kraje = {obec.get("kod"): (obec.find("Nazev").text, obec.get("okres")[0:2]) for obec in root.iter('Obec')}

		for ulice in root.iter('Ulice'):
			nazev = ulice.find("Nazev").text
			kod_ulice = ulice.get("kod")
			kod_obce = ulice.get("obec")
			nazev_obce = obce_kraje[kod_obce][0]
			kod_kraje = obce_kraje[kod_obce][1]
			nazev_kraje = min_values[kod_kraje][4]

			if min_values[kod_kraje][0] > len(nazev):
				min_values[kod_kraje] = (len(nazev), kod_ulice, nazev, nazev_obce, nazev_kraje)
			if max_values[kod_kraje][0] < len(nazev):
				max_values[kod_kraje] = (len(nazev), kod_ulice, nazev, nazev_obce, nazev_kraje)

		return list(min_values.values()), list(max_values.values())

	def run(self):
		"""
		Runs visualiser - gets information about streets with extreme names and converts it into geojson FeatureCollection.

		Calls find method for getting required information in 2 lists of lists and converts them into geojson FeatureCollection.

		Returns
		-------
		geojson.FeatureCollection
			FeatureCollestion containg MultiLines of shortest and longest streets
		"""
		(minimal_names, maximal_names) = self.find()
		return feature_collection_from_streets(minimal_names+maximal_names, self.db_tree, 'Extreme street names in region')
