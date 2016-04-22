import AddressVisualisation as AV

parser = AV.Parser()
parser.load('source/20141130_ST_UZSZ.xml')
parser.parse('database/') # output directory

visReg = AV.VisualiserRegistry()
visReg.setDatabasePath('databaase/')
visReg.registerVisualiserSet(AV.Visualisers.DefaultSet)
visReg.runVisualisers('visualised/') # output directory

generator = AV.Generator(input='visualised/', api=AV.GoogleMaps)
generator.generateHtml('index.html')
