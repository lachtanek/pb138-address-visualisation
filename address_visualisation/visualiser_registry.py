from .visualiser import Visualiser
import geojson
import logging
from xml.etree import cElementTree

class VisualiserRegistry:
	"""
	Registers and runs visualisers.
		
	...
	Attributes
	----------
	db_tree : cElementTree
		Tree from xml database in which visualisers will operate
	visualisers : list of (visualiser, output file name)
		List of registered visualisers and their output file names.
		
	Methods
	-------
	registerVisualiserSet(visualisers)
		Controls list of visualisers and registers them.
	registerVisualiser(VisClass, output_file_name)
		Controls visualiser and and registers it.
	runVisualisers(output_directory)
		Runs visualisers in `visualisers` attribute and saves their result into `output_directory`.
	"""
	def __init__(self, db_file):
		"""
		Class constructor.
		
		Creates cElementTree from `db_file` path and saves it to `db_tree` attribute.

		Parameters
		----------
		db_file : string
			Path to database xml
		"""
		self.db_tree = cElementTree.ElementTree(file=db_file)
		self.visualisers = []

	def registerVisualiserSet(self, visualisers):
		"""
		Controls visualisers and registers them.
		
		Checks visualisers in `visualisers` and adds them to `visualisers` class attribute.
		
		Parameters
		----------
		visualisers : list of (Visualiser, string)
			List of Visualier objects and their output filenames to check and register.
		
		Raises
		------
		Exception
			Type of argument is wrong.
		"""
		if not isinstance(visualisers, list):
			raise Exception('Argument must be instance of list')

		for (VisClass, output_file_name) in visualisers:
			self.registerVisualiser(VisClass, output_file_name)

	def registerVisualiser(self, VisClass, output_file_name):
		"""
		Controls visualiser and registers it.
		
		Checks if first item in `VisClass` is Visualiser.
		Adds visualiser and its output file name to `visualisers` class attribute.
		
		Parameters
		----------
		VisClass : Visualiser
			Visualiser to check and register.
		output_file_name : string
			Name of visualiser output file
			
		Raises
		------
		Exception
			Argument `VisClass` is not Visualiser.
		"""
		if not issubclass(VisClass, Visualiser):
			raise Exception('Argument must be subclass of Visualiser')

		self.visualisers.append((VisClass, output_file_name))

	def runVisualisers(self, output_directory):
		"""
		Runs Visualisers and saves their result into files in directory.
		
		Runs Visualisers from `visualisers`.
		Saves their result to json files in `output_directory` named by their filenames from `visualisers`.
				
		Parameters
		----------
		output_directory : string
			Path to directory with output files
		"""
		for (VisClass, output_file_name) in self.visualisers:
			logging.debug('Starting ' + VisClass.__name__)
			vis = VisClass(self.db_tree)
			output = vis.run()
			with open(output_directory + '/' + output_file_name + '.json', 'w') as f:
				f.write(geojson.dumps(output))
