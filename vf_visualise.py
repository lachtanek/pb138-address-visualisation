#!/usr/bin/python3
import geojson
from vf_visualiser.transformToFeatureCollection import feature_collection_from_streets

from vf_visualiser.longestStreets import LongestStreetsVisualiser
from vf_visualiser.extremeStreetNames import ExtremeStreetNamesVisualiser
from vf_visualiser.squareCount import SquareCountVisualiser
from vf_visualiser.biggestTowns import BiggestTownsVisualiser
from vf_visualiser.townWithMostStreets import TownWithMostStreetsVisualiser


output_directory = 'vf_visualiser/visualisations'

#streets
longest_streets_visualiser = LongestStreetsVisualiser('vf_simplified/simplified_stat.xml','vf_resources/db.xml')
longest_streets = longest_streets_visualiser.find()
with open(output_directory + '/' + 'longest_streets.json', 'w') as f:
	f.write(geojson.dumps(feature_collection_from_streets(longest_streets, 'vf_resources/db.xml', 'Longest streets in region')))

extreme_street_names_visualiser = ExtremeStreetNamesVisualiser('vf_simplified/simplified_stat.xml','vf_resources/db.xml')
(minimal_names, maximal_names) = extreme_street_names_visualiser.find()

min_f = open(output_directory + '/' + 'minimal_names.json', 'w')
min_f.write(geojson.dumps(feature_collection_from_streets(minimal_names, 'vf_resources/db.xml', 'Minimal street names in region')))
max_f = open(output_directory + '/' + 'maximal_names.json', 'w')
min_f.write(geojson.dumps(feature_collection_from_streets(maximal_names, 'vf_resources/db.xml', 'Maximal street names in region')))

#areas
square_count_visualiser = SquareCountVisualiser('vf_simplified/simplified_stat.xml','vf_resources/db.xml')
square_count = square_count_visualiser.find()
with open(output_directory + '/' + 'square_count.json', 'w') as f:
	f.write(geojson.dumps(feature_collection_from_areas(square_count, 'vf_resources/db.xml','vf_resources/db.xml', 'Square count in area')))

#towns
biggest_towns_visualiser = BiggestTownsVisualiser('vf_simplified/simplified_stat.xml','vf_simplified/simplified_obecbezulic.xml')
biggest_towns = biggest_towns_visualiser.find()
with open(output_directory + '/' + 'biggest_towns.json', 'w') as f:
	f.write(geojson.dumps(feature_collection_from_towns(biggest_towns, 'vf_resources/db.xml', 'Biggest towns in region')))

towns_with_most_streets_visualiser = TownWithMostStreetsVisualiser('vf_simplified/simplified_stat.xml','vf_resources/db.xml')
towns_with_most_streets = towns_with_most_streets_visualiser.find()
with open(output_directory + '/' + 'towns_with_most_streets.json', 'w') as f:
	f.write(geojson.dumps(feature_collection_from_towns(towns_with_most_streets, 'vf_resources/db.xml', 'Towns with most streets in region')))

