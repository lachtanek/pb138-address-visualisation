from abc import ABC, abstractmethod

class Visualiser(ABC):
	def __init__(self, db_tree):
		self.db_tree = db_tree

	@abstractmethod
	def run(self):
		pass
