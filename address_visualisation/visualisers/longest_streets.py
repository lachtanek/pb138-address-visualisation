#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_streets

class LongestStreetsVisualiser(Visualiser):
	"""
	Visualiser which finds streets with most address places in database xml and turns information about them into geojson format.

	...
	Methods
	-------
	find()
		Finds streets with most address places in region and returns information about them in list of lists.
	run()
		Calls find method and turns its result to geojson FeatureCollection.
	"""

	def find(self):
		"""
		Finds streets with most address places in each region in xml tree and returns information about its location.

		For each region, it searches through xml tree for towns in region and checks their number of address places.
		If this number is greater than maximum of region, method saves information about it into `max_values` on the position of region.

		Returns
		-------
		type
			list of lists

		max_values : list of lists
			For each region one list with following information about longest street in region:
			[number of address places, code of street, name of street, name of town, name of region]

		"""
		root = self.db_tree.getroot()

		kraje = root.findall(".//Kraj")
		max_values = {kraj.get("kod"): (0, None, None, None, kraj.find("Nazev").text) for kraj in kraje}

		obce = {obec.get("kod"): (obec.find("Nazev").text, obec.get("okres")[0:2]) for obec in root.iter('Obec')}

		for ulice in root.iter('Ulice'):
			pocet_adresnich_mist = int(ulice.find("PocetAdresnichMist").text)
			kod_obce = ulice.get("obec")
			kod_kraje = obce[kod_obce][1]
			nazev_obce = obce[kod_obce][0]

			if pocet_adresnich_mist > max_values[kod_kraje][0]:
				max_values[kod_kraje] = (pocet_adresnich_mist, ulice.get("kod"), ulice.find("Nazev").text, nazev_obce, max_values[kod_kraje][4])

		return list(max_values.values())

	def run(self):
		"""
		Runs visualiser - gets information about streets with most address places and converts it into geojson FeatureCollection.

		Calls find method for getting required information in list of lists and converts it into geojson FeatureCollection.

		Returns
		-------
		geojson.FeatureCollection
			FeatureCollection containing MultiLines of longest streets
		"""
		data = self.find()
		return feature_collection_from_streets(data, self.db_tree, 'Longest streets in region')
