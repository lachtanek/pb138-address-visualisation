#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_areas
from xml.etree import cElementTree

class SquareCountVisualiser(Visualiser):
	def run(self):
		tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
		tree_ulice = cElementTree.ElementTree(file=self.db_filepath)
		root = tree_stat.getroot()

		okresy = {okres.get("kod"): (0, okres.get("kod"), okres.find("Nazev").text) for okres in root.iter('Okres')}
		obce_okresy = {obec.get("kod"): obec.get("okres") for obec in root.iter('Obec')}

		for ulice in tree_ulice.iter('Ulice'):
			kod_obce = ulice.get("obec")
			kod_okresu = obce_okresy[kod_obce]

			nazev = ulice.find("Nazev").text
			if "nám" in nazev or "Nám" in nazev:
				(stary_pocet, _, nazev_okresu) = okresy[kod_okresu]
				okresy[kod_okresu] = (stary_pocet + 1, kod_okresu, nazev_okresu)

		return feature_collection_from_areas(okresy.values(), self.db_filepath, 'Square count in area')
