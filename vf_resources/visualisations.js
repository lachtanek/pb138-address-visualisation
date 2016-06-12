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

const formatLength = function(length) {
	if (length > 1000) {
		return (Math.round(length / 100) / 10) + ' km';
	} else {
		return Math.round(length) + ' m'
	}
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
			listInfo: streetListInfo,
			histogram: {
				plottedCategory: feature => feature.get('name'),
				style: {
					backgroundColor: 'rgba(0,0,0,0.2)',
					borderColor: 'rgba(0,0,0,1)',
					borderWidth: 1,
					hoverBackgroundColor: 'rgba(255,99,132,0.4)',
					hoverBorderColor: 'rgba(255,99,132,1)'
				}
			}
		}
	],
	[
		'longest_streets',
		{
			name: 'Nejdelší ulice',
			info: function(feature) {
				return `Ulice: ${feature.get('name')}<br>
				Město: ${feature.get('town')}<br>
				Délka: ${formatLength(feature.get('measured'))}`;
			},
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
			listInfo: areaListInfo,
			histogram: {
				partitions: [10, 20, 30, 40, 50, 60, 70, 80, 90]
			}
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
