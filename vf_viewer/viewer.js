'use strict';

/**
 * Class counting occurrences of values.
 */
class Histogram {
	constructor() {
		this.frequencies = {};
	}

	clear() {
		for (let i in this.frequencies) {
			this.frequencies[i] = 0;
		}
	}

	/**
	 * Increase frequency of val in the histogram.
	 *
	 * @param {any} val – Value to be added to a histogram.
	 */
	addValue(val) {
		if (this.frequencies.hasOwnProperty(val)) {
			this.frequencies[val]++;
		} else {
			this.frequencies[val] = 1;
		}
	}

	/**
	 * Produce the list of categories counted by the histogram.
	 *
	 * @return {Array[any]} List of categories.
	 */
	get labels() {
		let labels = [];
		for (let i in this.frequencies) {
			labels.push(i);
		}
		return labels;
	}

	/**
	 * Produce the list of frequencies of the categories as counted by the histogram.
	 *
	 * @return {Array[Int]} List of frequencies.
	 */
	get occurrences() {
		let occurrences = [];
		for (let i in this.frequencies) {
			occurrences.push(this.frequencies[i]);
		}
		return occurrences;
	}
}


/**
 * Class counting occurrences of numerical values in specified intervals.
 */
class PartitionedHistogram extends Histogram {
	/**
	 * Create a histogram of number intervals.
	 *
	 * @param {array[number]} partitions – List of numbers that will partition the numbers.
	 */
	constructor(partitions) {
		super();
		this.partitions = partitions.slice().sort();
	}

	/**
	 * Find an interval to add a value to and increase its frequency.
	 *
	 * @param {number} val – Value to be added to a histogram.
	 */
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

	/**
	 * Produce the list of intervals counted by the histogram.
	 *
	 * @return {Array[any]} List of intervals.
	 */
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

	/**
	 * Produce the list of frequencies of the intervals as counted by the histogram.
	 *
	 * @return {Array[Int]} List of frequencies.
	 */
	get occurrences() {
		let occurrences = [];
		for (var i = 0; i <= this.partitions.length; i++) {
			occurrences.push(this.frequencies[i] || 0);
		}
		return occurrences;
	}
}


/**
 * Class representing a menu with a list of available visualisations.
 */
class SideBar {
	/**
	 * Create a sidebar
	 *
	 * @param {Element} sideBarElement – An element to which the menu should be placed.
	 */
	constructor(sideBarElement) {
		this.sideBarElement = sideBarElement;
		const header = document.createElement('h1');
		header.textContent = 'Available visualisations';
		sideBarElement.appendChild(header);

		const visList = document.createElement('ul');
		sideBarElement.appendChild(visList);

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
		sideBarToggle.addEventListener('click', () => sideBarElement.classList.toggle('collapsed'));
		sideBarToggle.textContent = 'Menu';
		sideBarElement.appendChild(sideBarToggle);
	}

	/**
	 * Collapse the sidebar to save space on the screen.
	 */
	collapse() {
		this.sideBarElement.classList.add('collapsed');
	}

	/**
	 * Expand the sidebar so the user could change the visualisation.
	 */
	expand() {
		this.sideBarElement.classList.remove('collapsed');
	}
}

/**
 * A graphical representation of a Histogram using Chart.js.
 */
class HistoChart {
	/**
	 * Create a chart.
	 *
	 * @param {Canvas} canvas – A canvas element used for painting the chart.
	 */
	constructor(canvas, style) {
		this.chart = null;
		this.chartHolder = canvas;

		this.initStyle(style);
	}

	/**
	 * Initialise a chart style with specified properties.
	 *
	 * Following properties are supported:
	 * - backgroundColor
	 * - borderColor
	 * - borderWidth
	 * - hoverBackgroundColor
	 * - hoverBorderColor
	 *
	 * @param {Object} style – A dictionary defining values of the properties.
	 */
	initStyle(style = {}) {
		this.style = {
			backgroundColor: 'rgba(255,99,132,0.2)',
			borderColor: 'rgba(255,99,132,1)',
			borderWidth: 1,
			hoverBackgroundColor: 'rgba(255,99,132,0.4)',
			hoverBorderColor: 'rgba(255,99,132,1)'
		};

		for (let prop in this.style) {
			if (style.hasOwnProperty(prop)) {
				this.style[prop] = style[prop];
			}
		}
	}

	/**
	 * Update the chart data.
	 *
	 * @param {Histogram} histogram – A histogram that should be visualised.
	 */
	update(histogram) {
		if (!this.chart) {
			this.chart = new Chart(this.chartHolder, {
				type: 'bar',
				data: {
					labels: histogram.labels,
					datasets: [
						{
							backgroundColor: this.style.backgroundColor,
							borderColor: this.style.borderColor,
							borderWidth: this.style.borderWidth,
							hoverBackgroundColor: this.style.hoverBackgroundColor,
							hoverBorderColor: this.style.hoverBorderColor,
							data: histogram.occurrences,
						}
					]
				},
				options: {
					legend: {
						display: false
					},
					scales: {
						yAxes: [{
							ticks: {
								beginAtZero: true
							}
						}]
					}
				}
			});
		} else {
			for (let i in this.chart.data.datasets[0].data) {
				this.chart.data.datasets[0].data[i] = histogram.occurrences[i];
			}
			this.chart.update();
		}
	}
}

/**
 * Class representing a sidebar where a list of currently visible features,
 * as well as informations about the selected feature are displayed.
 */
class InfoBar {
	/**
	 * Create an info sidebar.
	 *
	 * @param {Element} infoBar – An element to which the sidebar should be placed.
	 * @param {Object} visualisation – Currently active visualisation.
	 */
	constructor(infoBar, visualisation) {
		this.visualisation = visualisation;

		this.infoHolder = document.createElement('div');
		this.infoHolder.classList.add('info');
		infoBar.appendChild(this.infoHolder);

		const featureHolder = document.createElement('div');
		infoBar.appendChild(featureHolder);

		this.header = document.createElement('h1');
		this.header.textContent = 'Visible features';
		featureHolder.classList.add('features');
		featureHolder.appendChild(this.header);

		this.emptyMessage = document.createElement('p');
		this.emptyMessage.textContent = 'There are no features in the visible area. Try zooming out or moving the map view.';
		this.emptyMessage.classList.add('hidden');
		featureHolder.appendChild(this.emptyMessage);

		this.featList = document.createElement('ul');
		featureHolder.appendChild(this.featList);

		this.chartEnabled = visualisation.histogram;
		this.histogram = null;

		if (this.chartEnabled) {
			if (visualisation.histogram.partitions) {
				this.histogram = new PartitionedHistogram(visualisation.histogram.partitions);
			} else {
				this.histogram = new Histogram;
			}

			this.plottedCategory = visualisation.histogram.plottedCategory || (feature => feature.get('measured'));

			const chartHolder = document.createElement('canvas');
			chartHolder.classList.add('chart');
			chartHolder.width = infoBar.offsetWidth;
			chartHolder.height = Math.floor(infoBar.offsetWidth / 16 * 9); // Chart will follow 16:9 ratio

			this.chart = new HistoChart(chartHolder, visualisation.histogram.style);

			infoBar.appendChild(chartHolder);
		}
	}

	/**
	 * Set the information about the selected feature.
	 *
	 * @param {String} info – Feature information.
	 */
	setInfo(info) {
		this.infoHolder.innerHTML = info;
	}

	/**
	 * Clear the information after the feature was deselected.
	 */
	clearInfo() {
		this.infoHolder.innerHTML = 'Hover a feature on the map or click on one in the list below to show information about the feature.';
	}

	/**
	 * Update the list of features.
	 *
	 * @param {Array[ol.Feature]} features – List of features to be listed.
	 * @param {Function} highlightFeature – A function that will highlight the feature selected in the list.
	 */
	setFeatures(features, highlightFeature) {
		this.featList.textContent = '';

		if (this.chartEnabled) {
			this.histogram.clear();
		}

		if (features.length == 0) {
			this.header.classList.add('hidden');
			this.emptyMessage.classList.remove('hidden');
		} else {
			this.header.classList.remove('hidden');
			this.emptyMessage.classList.add('hidden');
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

			if (this.chartEnabled) {
				this.histogram.addValue(this.plottedCategory(feature));
			}

			li.textContent = this.visualisation.listInfo(feature);
			this.featList.appendChild(li);
		});

		if (this.chartEnabled) {
			this.chart.update(this.histogram);
		}
	}
}

window.onload = function() {
	const fileName = window.location.search.toString().replace(/^\?/, '');
	const sideBar = new SideBar(document.getElementById('sidebar'));

	if (!fileName) {
		sideBar.expand();
	} else if (!visualisations.has(fileName)) {
		alert('Unknown visualisation.');
		window.location.search = '';
	} else {
		const currentVisualiser = visualisations.get(fileName);
		const infoBar = new InfoBar(document.getElementById('infobar'), currentVisualiser);

		document.title = 'Address visualisation – ' + currentVisualiser.name;
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
				infoBar.setInfo(currentVisualiser.info(feature))
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
