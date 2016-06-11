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
	],
	[
		'longest_streets',
		{
			name: 'Nejdelší ulice',
		}
	],
	[
		'extreme_street_names',
		{
			name: 'Ulice s extrémními jmény',
		}
	],
	[
		'square_count',
		{
			name: 'Počet náměstí',
		}
	],
	[
		'biggest_towns',
		{
			name: 'Největší města',
		}
	],
	[
		'town_with_most_streets',
		{
			name: 'Města s nejvíce ulicemi',
		}
	],
]);
