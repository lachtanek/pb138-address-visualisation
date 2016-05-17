const visualisations = new Map([
	[
		'sample_streets',
		{
			name: 'Ulice',
			info: function(feature) {
				return `${feature.getId()}: ${feature.get('name')}<br>
				${Math.round(feature.get('length'))} m`;
			}
		}
	]
]);
