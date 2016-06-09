#!/usr/bin/python3
from address_visualisation import Visualiser
from address_visualisation.features import FeatureCollection
from geojson import Feature, MultiLineString
from address_visualisation.helpers import multi_segment_length, parse_street_lines

class SampleStreetsVisualiser(Visualiser):
	__title = 'Ulice'

	def run(self):
		streets = []

		for street in self.db_tree.findall(".//Ulice"):
			street_id = int(street.get('kod'))
			segments = parse_street_lines(street.findall('Geometrie/PosList'))

			mls = MultiLineString(segments)
			length = multi_segment_length(segments)
			street_feature = Feature(geometry=mls, properties={'name': street.find('Nazev').text, 'length': length}, id=street_id)
			streets.append(street_feature)

		return FeatureCollection(self.__title, streets)
