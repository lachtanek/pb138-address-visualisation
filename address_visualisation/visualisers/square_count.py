#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_areas

class SquareCountVisualiser(Visualiser):
	def run(self):
		"""
		Finds areas with most squares and converts information about them to geojson FeatureCollection.
		
		For each region, it searches through xml tree for streets with 'nám' or 'Nám' in name and conts them.
		The counts and information about areas are saved into 'okresy' and converted into geojson FeatureCollection.
		
		Returns
		-------
		geojson.FeatureCollection
			FeatureCollection containing Polygons of towns with most squares
		"""
		root = self.db_tree.getroot()

		okresy = {okres.get("kod"): (0, okres.get("kod"), okres.find("Nazev").text) for okres in root.iter('Okres')}
		obce_okresy = {obec.get("kod"): obec.get("okres") for obec in root.iter('Obec')}

		for ulice in root.iter('Ulice'):
			kod_obce = ulice.get("obec")
			kod_okresu = obce_okresy[kod_obce]

			nazev = ulice.find("Nazev").text
			if "nám" in nazev or "Nám" in nazev:
				(stary_pocet, _, nazev_okresu) = okresy[kod_okresu]
				okresy[kod_okresu] = (stary_pocet + 1, kod_okresu, nazev_okresu)

		return feature_collection_from_areas(okresy.values(), self.db_tree, 'Square count in area')