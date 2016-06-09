from .visualiser import Visualiser
import geojson

class VisualiserRegistry:
	def __init__(self, stat_file, db_file):
		self.stat_file = stat_file
		self.db_file = db_file
		self.visualisers = []

	def registerVisualiserSet(self, visualisers):
		if not isinstance(visualisers, list):
			raise Exception('Argument must be instance of list')

		for (VisClass, output_file_name) in visualisers:
			self.registerVisualiser(VisClass, output_file_name)

	def registerVisualiser(self, VisClass, output_file_name):
		if not issubclass(VisClass, Visualiser):
			raise Exception('Argument must be subclass of Visualiser')

		self.visualisers.append((VisClass, output_file_name))

	def runVisualisers(self, output_directory):
		for (VisClass, output_file_name) in self.visualisers:
			vis = VisClass(self.stat_file, self.db_file)
			output = vis.run()
			with open(output_directory + '/' + output_file_name + '.json', 'w') as f:
				f.write(geojson.dumps(output))
