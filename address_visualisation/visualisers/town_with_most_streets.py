#!/usr/bin/python3
"""
Module with visualiser of towns with most streets in database.
"""

from address_visualisation import Visualiser
from address_visualisation.transform_to_feature_collection import feature_collection_from_towns

class TownWithMostStreetsVisualiser(Visualiser):
	"""
	Visualiser which finds towns with most streets in database xml and turns information about them into geojson format.

	...
	Methods
	-------
	find()
		Finds towns with most streets in region and returns information about them in list of lists.
	run()
		Calls find method and converts its result to geojson FeatureCollection.
	"""
	def find(self):
		"""
		Finds towns with most streets in each region in xml tree and returns information about its location.

		For each region, it searches through xml tree for towns in region and checks their number of streets.
		If this number is greater than maximum of region, method saves information about it into `max_values` on the position of region.

		Returns
		-------
		type
			list of lists

		max_values : list of lists
			For each region one list with following information about town with most streets in region:
			[number of address places, code of town, name of town, name of region]

		"""
		root = self.db_tree.getroot()

		kraje = root.findall(".//Kraj")
		max_values = {kraj.get("kod"): (0, None, None, kraj.find("Nazev").text) for kraj in kraje}

		obce = {obec.get("kod"): (0, obec.find("Nazev").text, obec.get("okres")[0:2]) for obec in root.iter('Obec')}

		for ulice in root.iter("Ulice"):
			kod_obce = ulice.get("obec")
			obce[kod_obce] = (obce[kod_obce][0] + 1, obce[kod_obce][1], obce[kod_obce][2])

		for kod_obce, obec in obce.items():
			pocet_ulic = obec[0]
			nazev_obce = obec[1]
			kod_kraje = obec[2]
			if pocet_ulic > max_values[kod_kraje][0]:
				nazev_kraje = max_values[kod_kraje][3]
				max_values[kod_kraje] = (pocet_ulic, kod_obce, nazev_obce, nazev_kraje)

		return list(max_values.values())

	def run(self):
		"""
		Runs visualiser - gets information about towns with most streets and converts it into geojson FeatureCollection.

		Calls find method to get required information in list of lists and converts this information into geojson FeatureCollection.

		Returns
		-------
		geojson.FeatureCollection
			FeatureCollection containing MultiLines of longest streets
		"""
		data = self.find()
		return feature_collection_from_towns(data, self.db_tree, 'Towns with most streets in region')
