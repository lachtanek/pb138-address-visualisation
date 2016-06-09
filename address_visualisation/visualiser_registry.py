from .visualiser import Visualiser

class VisualiserRegistry:
	def __init__(self, stat_file, db_file):
		self.stat_file = stat_file
		self.db_file = db_file
		self.visualisers = []

	def registerVisualiserSet(self, visualisers):
		if not isinstance(visualisers, list):
			raise Exception('Argument must be instance of list')

		for VisClass in visualisers:
			self.registerVisualiser(VisClass)

	def registerVisualiser(self, VisClass):
		if not issubclass(VisClass, Visualiser):
			raise Exception('Argument must be subclass of Visualiser')

		self.visualisers.append(VisClass)

	def runVisualisers(self, output_directory):
		for VisClass in self.visualisers:
			vis = VisClass(self.stat_file, self.db_file)
			vis.run(output_directory)
