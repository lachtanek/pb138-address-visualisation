#!/usr/bin/python3

from address_visualisation import Visualiser
from subprocess import call

class JavaVisualiser(Visualiser):
	"""
	Example base class for visualisers written in Java
	"""

	def __init__(self, arg1, arg2, jarFile):
		super().__init__(arg1, arg2)
		self.jarfile = jarFile

	def run(self, output_directory):
		call( [ 'java', '-jar', self.jarFile, self.stat_filepath, self.db_filepath, output_directory ] )
