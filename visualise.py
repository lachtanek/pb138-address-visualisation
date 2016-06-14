#!/usr/bin/python3
"""
Runs logging and visualiserRegistry for available visualisers.
"""
import address_visualisation as AV
from address_visualisation.visualisers import ProfaneStreetsVisualiser, BiggestTownsVisualiser, ExtremeStreetNamesVisualiser, LongestStreetsVisualiser, SquareCountVisualiser, TownWithMostStreetsVisualiser
import logging
import sys

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

DEFAULT_VISUALISERS = [
	(ProfaneStreetsVisualiser, 'profane_streets'),
	(BiggestTownsVisualiser, 'biggest_towns'),
	(ExtremeStreetNamesVisualiser, 'extreme_street_names'),
	(LongestStreetsVisualiser, 'longest_streets'),
	(SquareCountVisualiser, 'square_count'),
	(TownWithMostStreetsVisualiser, 'town_with_most_streets')
]

visualisers = []
if len(sys.argv) > 1:
	for a in sys.argv[1:]:
		s = a.split('=', 1)
		if len(s) != 2:
			raise Exception('Argument has to be in the form XxxVisualiser=output_name.')
		v = globals()[s[0]]
		if not issubclass(v, AV.Visualiser):
			raise Exception('The class name has to be an instance of visualiser.')
		if s[1].find('/') != -1:
			raise Exception('The output file name cannot contain a forward slash.')

		visualisers.append((v, s[1]))
else:
	visualisers = DEFAULT_VISUALISERS

visreg = AV.VisualiserRegistry('resources/db.xml')
visreg.register_visualiser_set(visualisers)
visreg.run_visualisers('resources/visualisations')
