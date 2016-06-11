const townInfo = function(feature, measured='Počet') {
	return `Město: ${feature.get('name')}<br>
	Kraj: ${feature.get('region')}<br>
	${measured}: ${feature.get('measured')}`;
}

const streetInfo = function(feature, measured='Počet') {
	return `Ulice: ${feature.get('name')}<br>
	Město: ${feature.get('town')}<br>
	${measured}: ${feature.get('measured')}`;
}

const areaInfo = function(feature, measured='Počet') {
	return `Okres: ${feature.get('name')}<br>
	${measured}: ${feature.get('measured')}`;
}

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
			info: (feature) => streetInfo(feature, 'Počet adresních míst')
		}
	],
	[
		'extreme_street_names',
		{
			name: 'Ulice s extrémními jmény',
			info: (feature) => streetInfo(feature, 'Délka')
		}
	],
	[
		'square_count',
		{
			name: 'Počet náměstí',
			info: (feature) => areaInfo(feature, 'Počet náměstí')
		}
	],
	[
		'biggest_towns',
		{
			name: 'Největší města',
			info: (feature) => townInfo(feature, 'Počet adresních míst')
		}
	],
	[
		'town_with_most_streets',
		{
			name: 'Města s nejvíce ulicemi',
			info: (feature) => townInfo(feature, 'Počet ulic')
		}
	],
]);
