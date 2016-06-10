#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_streets

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
		If their name is shorter than minimum or longer than maximum of region, it saves information about it into `minimum`/`maximum`.
		Finally, extreme values in `minimum` and `maximum` are saved into `min_values`,`max_values`.

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
		max_values = [None]*len(kraje)
		min_values = [None]*len(kraje)
		i = 0
		for kraj in kraje:
			minimum = [257, None, None, None, None]
			maximum = [-1, None, None, None, None]
			for okres in root.iter('Okres'):
				if okres.get("kod")[0:2] == kraj.get("kod"):
					for obec in root.iter('Obec'):
						if obec.get("okres") == okres.get("kod"):
							for ulice in root.iter('Ulice'):
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
		"""
		Runs visualiser - gets information about streets with extreme names and converts it into geojson FeatureCollection.

		Calls find method for getting required information in 2 lists of lists and converts them into geojson FeatureCollection.

		Returns
		-------
		type : geojson.FeatureCollection
		"""
		(minimal_names, maximal_names) = self.find()
		return feature_collection_from_streets(minimal_names+maximal_names, self.db_tree, 'Extreme street names in region')
