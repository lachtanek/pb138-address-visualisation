#!/usr/bin/python3
"""
Module with visualiser of longest streets in database.
"""

from address_visualisation.transform_to_feature_collection import feature_collection_from_streets, multi_segment_length, parse_street_lines
from address_visualisation import Visualiser

class LongestStreetsVisualiser(Visualiser):
	"""
	Visualiser which finds the longest streets in database xml and turns information about them into geojson format.

	...
	Methods
	-------
	find()
		Finds the longest streets in region and returns information about them in list of lists.
	run()
		Calls find method and turns its result to geojson FeatureCollection.
	"""

	def find(self):
		"""
		Finds the longest streets in each region in xml tree and returns information about their location.

		For each region, it searches through xml tree for streets in the region and checks their length.
		If this length is greater than the current maximum of the region, the maximum is updated.

		Returns
		-------
		type
			list of tuples

		max_values : list of tuples
			For each region one tuple with following information about longest street in region:
			(length in metres, code of street, name of street, name of town, name of region)

		"""
		root = self.db_tree.getroot()

		kraje = root.findall(".//Kraj")
		max_values = {kraj.get("kod"): (0, None, None, None, kraj.find("Nazev").text) for kraj in kraje}

		obce = {obec.get("kod"): (obec.find("Nazev").text, obec.get("okres")[0:2]) for obec in root.iter('Obec')}

		for ulice in root.iter('Ulice'):
			length = multi_segment_length(parse_street_lines(ulice.findall('Geometrie/PosList')))
			kod_obce = ulice.get("obec")
			kod_kraje = obce[kod_obce][1]
			nazev_obce = obce[kod_obce][0]

			if length > max_values[kod_kraje][0]:
				max_values[kod_kraje] = (length, ulice.get("kod"), ulice.find("Nazev").text, nazev_obce, max_values[kod_kraje][4])

		return list(max_values.values())

	def run(self):
		"""
		Runs visualiser – gets information about the longest streets and converts it into geojson FeatureCollection.

		Calls find method for getting required information in list of tuples and converts it into geojson FeatureCollection.

		Returns
		-------
		geojson.FeatureCollection
			FeatureCollection containing MultiLines of longest streets
		"""
		data = self.find()
		return feature_collection_from_streets(data, self.db_tree, 'Longest streets in region')
