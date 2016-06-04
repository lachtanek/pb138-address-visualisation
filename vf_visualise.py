#!/usr/bin/python3
import geojson
import transformToFeatureCollection

from longestStreets import LongestStreetsVisualiser
from extremeStreetNames import ExtremeStreetNamesVisualiser
from squareCount import SquareCountVisualiser
from biggestTowns import BiggestTownsVisualiser
from townWithMostStreets import TownWithMostStreetsVisualiser


output_directory = 'vf_visualiser/visualisations'

#streets	
longest_streets_visualiser = LongestStreetsVisualiser('vf_simplified/simplified_stat.xml','vf_simplified/simplified_obec_kompetni.xml')
longest_streets = longest_streets_visualiser.find()
with open(output_directory + '/' + 'longest_streets.json', 'w') as f:
	f.write(geojson.dumps(transformToFeatureCollection.feature_collection_from_streets(longest_streets, 'vf_simplified/simplified_obec_kompetni.xml', 'Longest streets in region')))

extreme_street_names_visualiser = ExtremeStreetNamesVisualiser('vf_simplified/simplified_stat.xml','vf_simplified/simplified_obec_kompetni.xml')
extreme_street_names = extreme_street_names_visualiser.find()
with open(output_directory + '/' + 'extreme_street_names.json', 'w') as f:
	f.write(geojson.dumps(transformToFeatureCollection.feature_collection_from_streets(extreme_street_names, 'vf_simplified/simplified_obec_kompetni.xml', 'Extreme street names in region')))

#areas
square_count_visualiser = SquareCountVisualiser('vf_simplified/simplified_stat.xml','vf_simplified/simplified_obec_kompetni.xml')
square_count = square_count_visualiser.find()
with open(output_directory + '/' + 'square_count.json', 'w') as f:
	f.write(geojson.dumps(transformToFeatureCollection.feature_collection_from_areas(square_count, 'vf_simplified/simplified_obec_kompetni.xml','vf_simplified/simplified_obec_kompetni.xml', 'Square count in area')))

#towns
biggest_towns_visualiser = BiggestTownsVisualiser('vf_simplified/simplified_stat.xml','vf_simplified/simplified_obecbezulic.xml')
biggest_towns = biggest_towns_visualiser.find()
with open(output_directory + '/' + 'biggest_towns.json', 'w') as f:
	f.write(geojson.dumps(transformToFeatureCollection.feature_collection_from_towns(biggest_towns, 'vf_simplified/simplified_obec_kompetni.xml', 'Biggest towns in region')))

towns_with_most_streets_visualiser = TownWithMostStreetsVisualiser('vf_simplified/simplified_stat.xml','vf_simplified/simplified_obec_kompetni.xml')
towns_with_most_streets = towns_with_most_streets_visualiser.find()
with open(output_directory + '/' + 'towns_with_most_streets.json', 'w') as f:
	f.write(geojson.dumps(transformToFeatureCollection.feature_collection_from_towns(towns_with_most_streets, 'vf_simplified/simplified_obec_kompetni.xml', 'Towns with most streets in region')))

