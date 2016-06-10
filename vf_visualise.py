#!/usr/bin/python3
import address_visualisation as AV

visreg = AV.VisualiserRegistry('vf_resources/db.xml')
visreg.registerVisualiserSet(AV.Visualisers.DEFAULT_VISUALISERS)
visreg.runVisualisers('vf_visualiser/visualisations')
