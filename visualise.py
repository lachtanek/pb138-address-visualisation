#!/usr/bin/python3
"""
Runs logging and visualiserRegistry for available visualisers.
"""
import address_visualisation as AV
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

visreg = AV.VisualiserRegistry('resources/db.xml')
visreg.register_visualiser_set(AV.Visualisers.DEFAULT_VISUALISERS)
visreg.run_visualisers('resources/visualisations')
