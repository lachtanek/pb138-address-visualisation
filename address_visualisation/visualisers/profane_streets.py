#!/usr/bin/python3

from address_visualisation import Visualiser
from address_visualisation.features import FeatureCollection
from address_visualisation.helpers import parse_street_lines
from geojson import Feature, MultiLineString
import re

class ProfaneStreetsVisualiser(Visualiser):
	"""
	Visualiser which finds streets with morbid names in database xml and turns information about them into geojson format.

	...
	Methods
	-------
	run()
		Finds streets with morbid names and converts information about them to geojson FeatureCollection.
	"""

	__title = 'Morbidní ulice'
	# __profanity = re.compile('p[iíyý]č|kure?v|kokot|kret|debi|blb|ser|sr[áa][čnt]|chcan|č[ůu]r|prc|jeb|mrd|šuk|sex|erot', re.IGNORECASE)
	__profanity = re.compile('hřbitov|krchov|smrt|mrtv|pite?v|pohře?b|kremator|krema|umrl|urn|rake?v|oběšen|vysel|přejet|utop|pukl|nafoukl|mršin|mrch|rozkl[aá]d|rozlož|krypt|kafiler|mau[sz]ole|padl|kaufland|vra[hž]', re.IGNORECASE)

	def run(self):
		"""
		Finds all streets with names related to death and converts information about them to geojson FeatureCollection.

		It goes through the xml tree and looks for streets whose name contains words like 'Fallen' or 'Graveyard'.
		The locations of these streets are converted into geojson FeatureCollection.

		Returns
		-------
		geojson.FeatureCollection
			FeatureCollection containing Lines of morbid streets
		"""
		streets = []
		town_names = {obec.get("kod"): obec.find("Nazev").text for obec in self.db_tree.iter('Obec')}

		for street in self.db_tree.findall(".//Ulice"):
			street_name = street.find('Nazev').text
			if self.__profanity.match(street_name):
				street_id = int(street.get('kod'))
				town_id = street.get('obec')
				segments = parse_street_lines(street.findall('Geometrie/PosList'))

				mls = MultiLineString(segments)
				street_feature = Feature(geometry=mls, properties={'name': street_name, 'town': town_names[town_id], 'style': {'stroke': 'black'}}, id=street_id)
				streets.append(street_feature)

		return FeatureCollection(self.__title, streets)

