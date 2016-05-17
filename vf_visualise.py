#!/usr/bin/python3
import geojson

from vf_visualiser.sample_streets import SampleStreets

output_directory = 'vf_visualiser/visualisations'

all_streets = SampleStreets('vf_simplified/simplified_obec_kompetni.xml')
with open(output_directory + '/' + 'sample_streets.json', 'w') as f:
	f.write(geojson.dumps(all_streets.all_streets()))
