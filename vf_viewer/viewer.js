'use strict';

class Histogram {
	constructor() {
		this.frequencies = {};
	}

	clear() {
		for (let i in this.frequencies) {
			this.frequencies[i] = 0;
		}
	}

	addValue(val) {
		if (this.frequencies.hasOwnProperty(val)) {
			this.frequencies[val]++;
		} else {
			this.frequencies[val] = 1;
		}
	}

	get labels() {
		let labels = [];
		for (let i in this.frequencies) {
			labels.push(i);
		}
		return labels;
	}

	get occurences() {
		let occurences = [];
		for (let i in this.frequencies) {
			occurences.push(this.frequencies[i]);
		}
		return occurences;
	}
}

class PartitionedHistogram extends Histogram {
	constructor(partitions) {
		super();
		this.partitions = partitions.slice().sort();
	}

	addValue(val) {
		let partition = this.partitions.length;
		for (let i = 0; i < this.partitions.length; i++) {
			if (val <= this.partitions[i]) {
				partition = i;
				break;
			}
		}
		super.addValue(partition);
	}

	get labels() {
		if (this.partitions.length == 0) {
			return ['*'];
		}

		let labels = [];
		for (var i = 0; i < this.partitions.length; i++) {
			if (i == 0) {
				labels.push('≤' + this.partitions[i]);
			} else {
				labels.push((this.partitions[i - 1] + 1).toString() + '–' + this.partitions[i]);
			}
		}
		labels.push('>' + this.partitions[i - 1]);

		return labels;
	}

	get occurences() {
		let occurences = [];
		for (var i = 0; i <= this.partitions.length; i++) {
			occurences.push(this.frequencies[i] || 0);
		}
		return occurences;
	}
}

const createSideBar = function() {
	const sideBar = document.getElementById('sidebar');

	const header = document.createElement('h1');
	header.textContent = 'Available visualisations';
	sideBar.appendChild(header);

	const visList = document.createElement('ul');
	sideBar.appendChild(visList);

	visualisations.forEach((item, key) => {
		const li = document.createElement('li');

		const a = document.createElement('a');
		a.href = '?' + key;
		a.textContent = item.name;
		li.appendChild(a);

		visList.appendChild(li);
	});

	const sideBarToggle = document.createElement('span');
	sideBarToggle.setAttribute('role', 'button');
	sideBarToggle.setAttribute('tabindex', '0');
	sideBarToggle.classList.add('sidebar-toggle')
	sideBarToggle.addEventListener('click', () => sideBar.classList.toggle('collapsed'));
	sideBarToggle.textContent = 'Menu';
	sideBar.appendChild(sideBarToggle);

	const self = {
		collapse: () => sideBar.classList.add('collapsed'),
		expand: () => sideBar.classList.remove('collapsed'),
	}

	return self;
}

const createInfoBar = function(fileName) {
	const infoBar = document.getElementById('infobar');

	const infoHolder = document.createElement('div');
	infoHolder.classList.add('info');
	infoBar.appendChild(infoHolder);

	const featureHolder = document.createElement('div');
	infoBar.appendChild(featureHolder);

	const header = document.createElement('h1');
	header.textContent = 'Visible features';
	featureHolder.classList.add('features');
	featureHolder.appendChild(header);

	const featList = document.createElement('ul');
	featureHolder.appendChild(featList);

	const chartEnabled = visualisations.get(fileName).histogram;
	let histogram, plottedCategory, chart, chartHolder;
	let chartStyle = {
		backgroundColor: 'rgba(255,99,132,0.2)',
		borderColor: 'rgba(255,99,132,1)',
		borderWidth: 1,
		hoverBackgroundColor: 'rgba(255,99,132,0.4)',
		hoverBorderColor: 'rgba(255,99,132,1)'
	};

	if (chartEnabled) {
		if (visualisations.get(fileName).histogram.partitions) {
			histogram = new PartitionedHistogram(visualisations.get(fileName).histogram.partitions);
		} else {
			histogram = new Histogram;
		}

		let styleProperties = visualisations.get(fileName).histogram.style;
		if (styleProperties) {
			for (let prop in chartStyle) {
				if (styleProperties.hasOwnProperty(prop)) {
					chartStyle[prop] = styleProperties[prop];
				}
			}
		}

		plottedCategory = visualisations.get(fileName).histogram.plottedCategory || (feature => feature.get('measured'));

		chartHolder = document.createElement('canvas');
		chartHolder.classList.add('chart');
		chartHolder.width = infoBar.offsetWidth;
		chartHolder.height = Math.floor(infoBar.offsetWidth / 16 * 9);

		infoBar.appendChild(chartHolder);
	}

	const self = {
		setInfo: (info) => {infoHolder.innerHTML = info;},
		clearInfo: () => {infoHolder.innerHTML = 'Hover a feature on the map or click on one in the list below to show information about the feature.';},
		setFeatures: (features, highlightFeature) => {
			featList.textContent = '';

			if (chartEnabled) {
				histogram.clear();
			}

			features.forEach((feature) => {
				const li = document.createElement('li');
				const highlight = () => {
					highlightFeature(feature);
				};

				li.setAttribute('role', 'button');
				li.setAttribute('tabindex', '0');
				li.feature = feature;
				li.addEventListener('click', highlight);
				li.addEventListener('keypress', (e) => {
					if (e.key == 'Spacebar' || e.key == ' ' || e.key == 'Enter') {
						e.preventDefault();
						highlight();
					}
				});

				if (chartEnabled) {
					histogram.addValue(plottedCategory(feature));
				}

				li.textContent = visualisations.get(fileName).listInfo(feature);
				featList.appendChild(li);
			});

			if (chartEnabled) {
				if (!chart) {
					chart = new Chart(chartHolder, {
						type: 'bar',
						data: {
							labels: histogram.labels,
							datasets: [
								{
									backgroundColor: chartStyle.backgroundColor,
									borderColor: chartStyle.borderColor,
									borderWidth: chartStyle.borderWidth,
									hoverBackgroundColor: chartStyle.hoverBackgroundColor,
									hoverBorderColor: chartStyle.hoverBorderColor,
									data: histogram.occurences,
								}
							]
						},
						options: {
							legend: {
								display: false
							}
						}
					});
				} else {
					for (let i in chart.data.datasets[0].data) {
						chart.data.datasets[0].data[i] = histogram.occurences[i];
					}
					chart.update();
				}
			}
		}
	};

	self.clearInfo();
	return self;
}

window.onload = function() {
	const fileName = window.location.search.toString().replace(/^\?/, '');
	const sideBar = createSideBar();

	if (!fileName) {
		sideBar.expand();
	} else if (!visualisations.has(fileName)) {
		alert('Unknown visualisation.');
		window.location.search = '';
	} else {
		const infoBar = createInfoBar(fileName);

		document.title = 'Address visualisation – ' + visualisations.get(fileName).name;
		sideBar.collapse();
		setTimeout(() => document.body.classList.remove('preload'), 250);

		proj4.defs('urn:ogc:def:crs:EPSG::5514','+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=589,76,480,0,0,0,0 +units=m +no_defs');

		function styleFunction(feature) {
			let style;
			let fillColor = 'rgba(240, 0, 0, 0.3)';
			let strokeColor = 'rgba(240, 0, 0, 1)';

			let styleProperty = feature.get('style');
			if (styleProperty) {
				if (styleProperty.fill) {
					fillColor = styleProperty.fill;
				}
				if (styleProperty.stroke) {
					strokeColor = styleProperty.stroke;
				}
			}

			if (feature.getGeometry().getType() === 'Point') {
				style = new ol.style.Style({
					image: new ol.style.Circle({
						radius: 5,
						fill: new ol.style.Fill({
							color: fillColor,
						}),
						stroke: new ol.style.Stroke({
							color: strokeColor,
							width: 10
						})
					})
				});
			} else {
				style = new ol.style.Style({
					fill: new ol.style.Fill({
						color: fillColor,
					}),
					stroke: new ol.style.Stroke({
						color: strokeColor,
						width: 10
					})
				});
			}

			return style;
		}

		const geoJsonSource = new ol.source.Vector({
			url: '../vf_resources/visualisations/' + fileName + '.json',
			format: new ol.format.GeoJSON()
		});

		const map = new ol.Map({
			layers: [
				new ol.layer.Tile({
					source: new ol.source.OSM()
				}),
				new ol.layer.Image({
					source: new ol.source.ImageVector({
						source: geoJsonSource,
						style: styleFunction
					})
				})
			],
			target: 'view',
			view: new ol.View({
				center: ol.proj.fromLonLat([15.5, 49.75]),
				zoom: 8,
				minZoom: 8
			})
		});

		const featureOverlay = new ol.layer.Vector({
			source: new ol.source.Vector(),
			map: map,
			style: new ol.style.Style({
				stroke: new ol.style.Stroke({
					color: '#f0f000',
					width: 10
				}),
				fill: new ol.style.Fill({
					color: 'rgba(240,240,0,0.3)'
				})
			})
		});

		function getFeatureUnderCursor(pixel) {
			return map.forEachFeatureAtPixel(pixel, function(feature) {
				return feature;
			});
		}

		let highlight;
		function highlightFeature(feature) {
			if (feature) {
				infoBar.setInfo(visualisations.get(fileName).info(feature))
			} else {
				infoBar.clearInfo();
			}

			if (feature !== highlight) {
				if (highlight) {
					featureOverlay.getSource().removeFeature(highlight);
				}
				if (feature) {
					featureOverlay.getSource().addFeature(feature);
				}
				highlight = feature;
			}

		};

		map.on('pointermove', function(evt) {
			if (evt.dragging) {
				return;
			}
			const pixel = map.getEventPixel(evt.originalEvent);
			highlightFeature(getFeatureUnderCursor(pixel));
		});

		map.on('click', function(evt) {
			highlightFeature(getFeatureUnderCursor(evt.pixel));
		});

		function updateFeatureList() {
			const extent = map.getView().calculateExtent(map.getSize());
			const features = geoJsonSource.getFeaturesInExtent(extent);
			infoBar.setFeatures(features, highlightFeature);
		}

		geoJsonSource.once('change', () => map.on('postrender', updateFeatureList));
	}
};
