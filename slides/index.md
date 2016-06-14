---
title: Vizualizace adresních míst<br><small>PB138</small>
author: Jakub Hrabec, Alice Nohejlová, Jan Tojnar, Jana Zahradníčková
date: 2016-06-14
...

Demo
====

Transformace
============
> - [RÚIAN](http://vdp.cuzk.cz/)
> - Jak se měnila databáze?

Downloader
==========
> - Práce s větším objemem dat
> - Jak řešit rychlost vs. nároky?


Visualisace
===========
- 7 vizualizérů
- Vstup – XML databáze
- Výstup – GeoJSON soubory


Viewer
======
> - výstup visualisérů → znázornění na mapě
> - mapové vrstvy
> - kód projektu + první visualisér
> - vykreslování histogramů + seznam prvků
> - 9.5 min → 3.7 sec
> - refactoring

Poděkování
==========
- [OpenLayers](http://openlayers.org/) – drawing the geographical displaying the map
- [Chart.js](http://www.chartjs.org/) – drawing the histogram
- [Proj4js](http://proj4js.org/) – projecting the geographical data from EPSG:5514
- [OpenStreetMap](https://www.openstreetmap.org/) – map layers
- [python-geojson](https://pypi.python.org/pypi/geojson) – Python GeoJSON bindings
- [RÚIAN](http://www.cuzk.cz/ruian.aspx) – address database source

Diskuse
=======
