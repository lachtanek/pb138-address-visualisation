from abc import ABC, abstractmethod

class Visualiser(ABC):
	"""
	Class which finds information in database xml and converts it into geojson format.

	...
	Attributes
	----------
	db_tree : xml.etree.cElementTree
		cElementTree of xml with information
	
	Methods
	-------
	run()
		Finds information in `db_tree`and converts it into geojson FeatureCollection.
	"""
	def __init__(self, db_tree):
		"""
		Class constructor.

		Parameters
		----------
		db_tree : xml.etree.cElementTree
			cElementTree of xml with information
		"""
		self.db_tree = db_tree

	@abstractmethod
	def run(self):
		"""
		Finds information in xml database tree and converts it into geojson FeatureCollection.
		"""
		pass
