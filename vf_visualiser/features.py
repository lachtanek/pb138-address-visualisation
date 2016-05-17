class FeatureCollection():
	def __init__(self, name, features):
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

