#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_towns

class BiggestTownsVisualiser(Visualiser):
	def find(self):
		root = self.db_tree.getroot()
		kraje = root.findall(".//Kraj")
		maxValues = [None]*len(kraje)
		i = 0
		for kraj in kraje:
			maximum = (0, None, None, kraj.find("Nazev").text)
			for okres in root.iter('Okres'):
				if okres.get("kod")[0:2] == kraj.get("kod"):
					for obec in root.iter('Obec'):
						if obec.get("okres") == okres.get("kod"):
							for obec_ulice in root.iter('AdresniMista'):
								if obec_ulice.get("obec") == obec.get("kod"):
									pocet_adresnich_mist = int(obec_ulice.find("pocetAdresnichMist").text)
									if pocet_adresnich_mist > maximum[0]:
										maximum = (pocet_adresnich_mist, obec.get("kod"), obec.find("Nazev").text, kraj.find("Nazev").text)
			maxValues[i] = maximum
			i = i + 1
		return maxValues

	def run(self):
		data = self.find()
		return feature_collection_from_towns(data, self.db_tree, 'Biggest towns in region')
