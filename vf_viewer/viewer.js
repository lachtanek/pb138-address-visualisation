const fileName = window.location.search.toString().replace(/^\?/, '');

if (!fileName) {
	const view = document.getElementById('view');

	const header = document.createElement('h1');
	header.textContent = 'Available visualisations';
	view.appendChild(header);

	const menu = document.createElement('ul');
	view.appendChild(menu);

	visualisations.forEach((item, key) => {
		const li = document.createElement('li');

		const a = document.createElement('a');
		a.href = '?' + key;
		a.textContent = item.name;
		li.appendChild(a);

		menu.appendChild(li);
	})
} else if (!visualisations.has(fileName)) {
	alert('Unknown visualisation.');
	window.location.search = '';
} else {
	proj4.defs('urn:ogc:def:crs:EPSG::5514','+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=589,76,480,0,0,0,0 +units=m +no_defs');

	const pointStyle = new ol.style.Style({
		image: new ol.style.Circle({
			radius: 5,
			fill: new ol.style.Fill({
				color: 'rgba(240, 0, 0, 0.3)'
			}),
			stroke: new ol.style.Stroke({
				color: '#f00000',
				width: 10
			})
		})
	});

	const shapeStyle = new ol.style.Style({
		fill: new ol.style.Fill({
			color: 'rgba(240, 0, 0, 0.3)'
		}),
		stroke: new ol.style.Stroke({
			color: '#f00000',
			width: 10
		})
	});

	function styleFunction(feature) {
		if (feature.getGeometry().getType() === 'Point') {
			return pointStyle;
		} else {
			return shapeStyle;
		}
	}

	const map = new ol.Map({
		layers: [
			new ol.layer.Tile({
				source: new ol.source.OSM()
			}),
			new ol.layer.Image({
				source: new ol.source.ImageVector({
					source: new ol.source.Vector({
						url: '../vf_visualiser/visualisations/' + fileName + '.json',
						format: new ol.format.GeoJSON()
					}),
					style: styleFunction
				})
			})
		],
		target: 'view',
		view: new ol.View({
			center: ol.proj.fromLonLat([14.416667, 50.083333]),
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

	let highlight;
	const displayFeatureInfo = function(pixel) {
		const feature = map.forEachFeatureAtPixel(pixel, function(feature) {
			return feature;
		});

		const info = document.getElementById('info');
		if (feature) {
			info.innerHTML = visualisations.get(fileName).info ? visualisations.get(fileName).info(feature) : (feature.getId() + ': ' + feature.get('name'));
		} else {
			info.innerHTML = '';
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
		displayFeatureInfo(pixel);
	});

	map.on('click', function(evt) {
		displayFeatureInfo(evt.pixel);
	});
}
