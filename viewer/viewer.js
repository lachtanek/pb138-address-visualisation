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
 * Abstract class used for event handling
 * Taken from http://stackoverflow.com/a/24216547/160386
 */
class Emitter {
	constructor() {
		this.eventTarget = document.createDocumentFragment();
		['addEventListener', 'dispatchEvent', 'removeEventListener']
		.forEach(method => this[method] = this.eventTarget[method].bind(this.eventTarget));
	}
}


/**
 * Class representing a sidebar where a list of currently visible features,
 * as well as informations about the selected feature are displayed.
 */
class InfoBar extends Emitter {
	/**
	 * Create an info sidebar.
	 *
	 * @param {Element} infoBar – An element to which the sidebar should be placed.
	 * @param {Object} visualisation – Currently active visualisation.
	 */
	constructor(infoBar, visualisation) {
		super();
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
	 */
	setFeatures(features) {
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

			li.setAttribute('role', 'button');
			li.setAttribute('tabindex', '0');
			li.feature = feature;
			li.addEventListener('click', () => this.requestFeatureSelection(feature));
			li.addEventListener('keypress', (e) => {
				if (e.key == 'Spacebar' || e.key == ' ' || e.key == 'Enter') {
					e.preventDefault();
					this.requestFeatureSelection(feature);
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

	/**
	 * Emits an event requesting to app to select a feature.
	 *
	 * @param {ol.Feature} feature
	 * @emits InfoBar#select-feature
	 */
	requestFeatureSelection(feature) {
		const evt = new Event('select-feature');
		evt.feature = feature;
		this.dispatchEvent(evt);
	}

	/**
	 * If a feature is passed, information about it will be displayed.
	 *
	 * @param {ol.Feature} feature
	 */
	selectFeature(feature) {
		if (feature) {
			this.setInfo(this.visualisation.info(feature))
		} else {
			this.clearInfo();
		}
	}
}

/**
 * Class representing a canvas that will display the map layers
 * as well as draw the geographical features.
 */
class MapView extends Emitter {
	/**
	 * Create a map view
	 *
	 * @param {String} dataSource – Location of GeoJSON file.
	 * @param {Element} target – Element for rendering map.
	 */
	constructor(dataSource, target) {
		super();
		this.highlight = null;
		this.geoJsonSource = new ol.source.Vector({
			url: dataSource,
			format: new ol.format.GeoJSON()
		});

		this.map = new ol.Map({
			layers: [
				new ol.layer.Tile({
					source: new ol.source.OSM()
				}),
				new ol.layer.Image({
					source: new ol.source.ImageVector({
						source: this.geoJsonSource,
						style: this.styleFunction
					})
				})
			],
			target: target,
			view: new ol.View({
				center: ol.proj.fromLonLat([15.5, 49.75]),
				zoom: 8,
				minZoom: 8
			})
		});

		this.featureOverlay = new ol.layer.Vector({
			source: new ol.source.Vector(),
			map: this.map,
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

		this.map.on('pointermove', evt => {
			if (evt.dragging) {
				return;
			}
			const pixel = this.map.getEventPixel(evt.originalEvent);
			this.requestFeatureSelection(this.getFeatureUnderCursor(pixel));
		});

		this.map.on('click', evt => {
			this.requestFeatureSelection(this.getFeatureUnderCursor(evt.pixel));
		});

		this.geoJsonSource.once('change', () => this.map.on('postrender', () => this.updateFeatureList()));
	}

	/**
	 * Request the feature list to be updated.
	 *
	 * @emits MapView#update-features
	 */
	updateFeatureList() {
		const extent = this.map.getView().calculateExtent(this.map.getSize());
		const features = this.geoJsonSource.getFeaturesInExtent(extent);

		const evt = new Event('update-features');
		evt.features = features;
		this.dispatchEvent(evt);
	}

	/**
	 * Emits an event requesting to app to select a feature.
	 *
	 * @param {ol.Feature} feature
	 * @emits MapView#select-feature
	 */
	requestFeatureSelection(feature) {
		const evt = new Event('select-feature');
		evt.feature = feature;
		this.dispatchEvent(evt);
	}

	/**
	 * If a feature is passed, it will be highlighted on the map.
	 *
	 * @param {ol.Feature}
	 */
	selectFeature(feature) {
		if (feature !== this.highlight) {
			if (this.highlight) {
				this.featureOverlay.getSource().removeFeature(this.highlight);
			}
			if (feature) {
				this.featureOverlay.getSource().addFeature(feature);
			}
			this.highlight = feature;
		}
	}

	/**
	 * Creates style for displaying a feature on the map.
	 *
	 * @param {ol.Feature}
	 * @returns {ol.style.Style}
	 */
	styleFunction(feature) {
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

	/**
	 * Returns the feature located on the specified pixel.
	 *
	 * @param {ol.Pixel}
	 * @returns {o.Feature}
	 */
	getFeatureUnderCursor(pixel) {
		return this.map.forEachFeatureAtPixel(pixel, feature => feature);
	}
}

/**
 * Main application class
 */
class Viewer {
	/**
	 * Main function of the application.
	 * It prepares the side bars as well as map view and connects them using events.
	 *
	 * @param {Array[Object]} visualisations
	 * @param {String} fileName
	 * @param {Element} container
	 */
	constructor(visualisations, fileName, container) {
		const sideBar = this.createSideBar(visualisations, container);

		if (!fileName) {
			sideBar.expand();
		} else if (!visualisations.has(fileName)) {
			alert('Unknown visualisation.');
			window.location.search = '';
		} else {
			const visualisation = visualisations.get(fileName);
			this.infoBar = this.createInfoBar(visualisation, container);
			this.infoBar.addEventListener('select-feature', evt => this.selectFeature(evt.feature));

			this.setTitle(visualisation.name);
			sideBar.collapse();

			proj4.defs('urn:ogc:def:crs:EPSG::5514','+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=589,76,480,0,0,0,0 +units=m +no_defs');

			this.mapView = this.createMapView(fileName, container);
		}
	}

	/**
	 * Bootstraps a sidebar.
	 *
	 * @param {Array[Object]} visualisations
	 * @param {Element} container
	 * @returns {SideBar}
	 */
	createSideBar(visualisations, container) {
		const sideBarElement = document.createElement('div');
		sideBarElement.classList.add('sidebar');
		container.appendChild(sideBarElement);
		return new SideBar(sideBarElement, visualisations);
	}

	/**
	 * Bootstraps an infobar.
	 *
	 * @param {Object} visualisation
	 * @param {Element} container
	 * @returns {InfoBar}
	 */
	createInfoBar(visualisation, container) {
		const infoBarElement = document.createElement('div');
		infoBarElement.classList.add('infobar');
		container.appendChild(infoBarElement);
		return new InfoBar(infoBarElement, visualisation);
	}

	/**
	 * Bootstraps a map view.
	 *
	 * @param {String} fileName
	 * @param {Element} container
	 * @returns {MapView}
	 */
	createMapView(fileName, container) {
		const mapViewElement = document.createElement('div');
		mapViewElement.classList.add('view');
		container.appendChild(mapViewElement);

		const mapView = new MapView('../resources/visualisations/' + fileName + '.json', mapViewElement);
		mapView.addEventListener('update-features', evt => this.infoBar.setFeatures(evt.features));
		mapView.addEventListener('select-feature', evt => this.selectFeature(evt.feature));

		return mapView;
	}

	/**
	 * Sets the document title
	 */
	setTitle(title) {
		document.title = 'Address visualisation – ' + title;
	}

	/**
	 * Tell the map view and info bar to select given feature.
	 *
	 * @param {ol.Feature}
	 */
	selectFeature(feature) {
		this.infoBar.selectFeature(feature);
		this.mapView.selectFeature(feature);
	}
}

/**
 * Main function of the application, fired after the DOM was loaded.
 */
window.onload = () => {
	const fileName = window.location.search.toString().replace(/^\?/, '');
	const app = new Viewer(visualisations, fileName, document.body);
};
