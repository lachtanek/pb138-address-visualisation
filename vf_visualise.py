#!/usr/bin/python3
import address_visualisation as AV
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

visreg = AV.VisualiserRegistry('vf_resources/db.xml')
visreg.registerVisualiserSet(AV.Visualisers.DEFAULT_VISUALISERS)
visreg.runVisualisers('vf_visualiser/visualisations')
