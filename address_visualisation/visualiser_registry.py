"""
Registry of visualisers and names of their output files.
"""
from xml.etree import cElementTree
import logging
import geojson
from .visualiser import Visualiser

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

	def register_visualiser_set(self, visualisers):
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

		for (vis_class, output_file_name) in visualisers:
			self.register_visualiser(vis_class, output_file_name)

	def register_visualiser(self, vis_class, output_file_name):
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
		if not issubclass(vis_class, Visualiser):
			raise Exception('Argument must be subclass of Visualiser')

		self.visualisers.append((vis_class, output_file_name))

	def run_visualisers(self, output_directory):
		"""
		Runs Visualisers and saves their result into files in directory.

		Runs Visualisers from `visualisers`.
		Saves their result to json files in `output_directory` named by their filenames from `visualisers`.

		Parameters
		----------
		output_directory : string
			Path to directory with output files
		"""
		for (vis_class, output_file_name) in self.visualisers:
			logging.debug('Starting ' + vis_class.__name__)
			vis = vis_class(self.db_tree)
			output = vis.run()
			with open(output_directory + '/' + output_file_name + '.json', 'w') as output_file:
				output_file.write(geojson.dumps(output))
