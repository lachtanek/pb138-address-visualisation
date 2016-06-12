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

const streetListInfo = function(feature) {
	return `${feature.get('name')}, ${feature.get('town')}`;
}

const townListInfo = function(feature) {
	return `${feature.get('name')} (${feature.get('region')})`;
}

const areaListInfo = function(feature) {
	return feature.get('name');
}

const visualisations = new Map([
	[
		'profane_streets',
		{
			name: 'Morbidní ulice',
			info: function(feature) {
				return `Ulice: ${feature.get('name')}<br>
				Město: ${feature.get('town')}`;
			},
			listInfo: streetListInfo
		}
	],
	[
		'longest_streets',
		{
			name: 'Nejdelší ulice',
			info: (feature) => streetInfo(feature, 'Počet adresních míst'),
			listInfo: streetListInfo
		}
	],
	[
		'extreme_street_names',
		{
			name: 'Ulice s extrémními jmény',
			info: feature => streetInfo(feature, 'Délka'),
			listInfo: streetListInfo
		}
	],
	[
		'square_count',
		{
			name: 'Počet náměstí',
			info: feature => areaInfo(feature, 'Počet náměstí'),
			listInfo: areaListInfo
		}
	],
	[
		'biggest_towns',
		{
			name: 'Největší města',
			info: feature => townInfo(feature, 'Počet adresních míst'),
			listInfo: townListInfo
		}
	],
	[
		'town_with_most_streets',
		{
			name: 'Města s nejvíce ulicemi',
			info: feature => townInfo(feature, 'Počet ulic'),
			listInfo: townListInfo
		}
	],
]);
