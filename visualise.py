#!/usr/bin/python3
"""
Runs logging and visualiserRegistry for available visualisers.
"""
import address_visualisation as AV
from address_visualisation.visualisers import ProfaneStreetsVisualiser, BiggestTownsVisualiser, ExtremeStreetNamesVisualiser, LongestStreetsVisualiser, SquareCountVisualiser, TownWithMostStreetsVisualiser
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

DEFAULT_VISUALISERS = [
	(ProfaneStreetsVisualiser, 'profane_streets'),
	(BiggestTownsVisualiser, 'biggest_towns'),
	(ExtremeStreetNamesVisualiser, 'extreme_street_names'),
	(LongestStreetsVisualiser, 'longest_streets'),
	(SquareCountVisualiser, 'square_count'),
	(TownWithMostStreetsVisualiser, 'town_with_most_streets')
]

visualisers = DEFAULT_VISUALISERS

visreg = AV.VisualiserRegistry('resources/db.xml')
visreg.register_visualiser_set(visualisers)
visreg.run_visualisers('resources/visualisations')
