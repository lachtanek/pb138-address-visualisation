"""
Module with custom geojson FeatureCollection.
"""
class FeatureCollection:
	"""
	Creates geojson.FeatureCollection with custom structure.

	...

	Attributes
	----------
	name : string
		Name of FeatureCollection
	features : list of geojson.Feature
		List of Features in FeatureCollection
	"""
	def __init__(self, name, features):
		"""
		Class constructor.

		Parameters
		----------
		name : string
			Name of FeatureCollection
		features : list of geojson.Feature
			List of Features in FeatureCollection
		"""
		self.name = name
		self.features = features

	@property
	def __geo_interface__(self):
		return {
			'type': 'FeatureCollection',
			'properties': {
				'name': self.name
			},
			'crs': {
				'type': 'name',
				'properties': {
					'name': 'urn:ogc:def:crs:EPSG::5514'
				}
			},
			'features': self.features
		}
