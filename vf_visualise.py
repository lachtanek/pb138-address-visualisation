#!/usr/bin/python3
import address_visualisation as AV

visreg = AV.VisualiserRegistry('vf_resources/db.xml')
visreg.registerVisualiserSet(AV.Visualisers.DefaultSet)
visreg.runVisualisers('vf_visualiser/visualisations')

