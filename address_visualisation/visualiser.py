from abc import ABC, abstractmethod

class Visualiser(ABC):
	def __init__(self, stat_filepath, db_filepath):
		self.stat_filepath = stat_filepath
		self.db_filepath = db_filepath

	@abstractmethod
	def run(self):
		pass
