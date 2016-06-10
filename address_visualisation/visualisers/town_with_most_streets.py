#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_towns

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
		If this number is greater than maximum of region, method saves information about it into `maximum`.
		Finally, extreme values in `maximum` are saved into `maxValues`.

		Returns
		-------
		type
			list of lists

		max_values : list of lists
			For each region one array with following information about town with most streets in region:
			[number of address places, code of town, name of town, name of region]

		"""
		root = self.db_tree.getroot()
		kraje = root.findall(".//Kraj")
		max_values = [None]*len(kraje)
		i = 0
		for kraj in kraje:
			maximum = [0,None,None,None,kraj.find("Nazev").text]
			for okres in root.iter('Okres'):
				if okres.get("kod")[0:2] == kraj.get("kod"):
					for obec in root.iter('Obec'):
						if obec.get("okres") == okres.get("kod"):
							count = 0
							for ulice in root.iter('Ulice'):
								if ulice.get("obec") == obec.get("kod"):
									count = count + 1
							if count > maximum[0]:
								maximum = [count, obec.get("kod"), obec.find("Nazev").text, kraj.find("Nazev").text]
			max_values[i] = maximum
			i = i + 1

		return max_values

	def run(self):
		"""
		Runs visualiser - gets information about towns with most streets and converts it into geojson FeatureCollection.

		Calls find method to get required information in list of lists and converts this information into geojson FeatureCollection.

		Returns
		-------
		type : geojson.FeatureCollection
		"""
		data = self.find()
		return feature_collection_from_towns(data, self.db_tree, 'Towns with most streets in region')
