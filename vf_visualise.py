#!/usr/bin/python3
import address_visualisation as AV

visreg = AV.VisualiserRegistry('vf_simplified/simplified_stat.xml', 'vf_resources/db.xml')
visreg.registerVisualiserSet(AV.Visualisers.DefaultSet)
visreg.runVisualisers('vf_visualiser/visualisations')

