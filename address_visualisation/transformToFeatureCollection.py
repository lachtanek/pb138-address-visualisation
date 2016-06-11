from geojson import Feature, MultiLineString, Point, Polygon
from .features import FeatureCollection
from .helpers import multi_segment_length, parse_street_lines, parse_segment, get_color

class Street:
	"""
	Enumeration of indices in list of information about street.

	Attributes
	----------
	measured : int
		index of measured information in the street
	code : int
		index of code of the street
	street_name : int
		index of name of the street
	town_name : int
		index of name of the town where the street is situated
	region_name : int
		index of name of the region where the street is situated
	"""
	measured = 0
	code = 1
	street_name = 2
	town_name = 3
	region_name = 4

class Town:
	"""
	Enumeration of indices in list of information about town.

	Attributes
	----------
	measured : int
		index of measured information in the town
	code : int
		index of code of the town
	town_name : int
		index of name of the town
	region_name : int
		index of name of the region where the town is situated
	"""
	measured = 0
	code = 1
	town_name = 2
	region_name = 3

class Area:
	"""
	Enumeration of indices in list of information about area.

	Attributes
	----------
	measured : int
		index of measured information in the area
	code : int
		index of code of the area
	area_name : int
		index of name of the area
	"""
	measured = 0
	code = 1
	area_name = 2


def feature_collection_from_streets(values, street_tree, collection_title):
	"""
	Transformation of information about streets into gejson FeatureCollection.

	Parameters
	----------
	values : list of lists
		List of information about one street of each region in following format:
		[measured value, code of street, name of street, name of town, name of region]
	db_tree : xml.etree.cElementTree
		cElementTree of xml database about contry addresses
	collection_title : string
		What name the resulting FeatureCollection should have.

	Returns
	-------
	geojson.FeatureCollection
		FeatureCollection containing MultiLines made from information about streets from `values`.
	"""
	streets_collection = []
	for region_street in values:
		street_positions = street_tree.getroot().findall(".//Ulice[@kod='"+region_street[1]+"']/Geometrie/PosList")
		lines = parse_street_lines(street_positions)

		mls = MultiLineString(lines)
		length = multi_segment_length(lines)
		street_feature = Feature(geometry=mls, properties={'name': region_street[Street.street_name], 'town': region_street[Street.town_name], 'region': region_street[Street.region_name], 'length': length, 'measured': region_street[Street.measured]}, id=int(region_street[Street.code]))
		streets_collection.append(street_feature)

	return FeatureCollection(collection_title, streets_collection)

def feature_collection_from_towns(values, street_tree, collection_title):
	"""
	Transformation of information about towns into gejson FeatureCollection.

	Transformation of information about towns into gejson FeatureCollection.
	Method finds location of street, creates Polygon, and Feature with properties which contains Polygon, and adds it into list `towns_collection`.
	From `towns_collection`, it creates FeatureCollection.

	Parameters
	----------
	values : list of lists
		List of information about one town of each region in following format:
		[measured value, code of town, name of town, name of region]
	db_tree : xml.etree.cElementTree
		cElementTree of xml database about contry addresses
	collection_title : string
		What name the resulting FeatureCollection should have.

	Returns
	-------
	geojson.FeatureCollection
		FeatureCollection containing Polygons made from information about towns from `values`.
	"""
	towns_collection = []
	for region_town in values:
		town_positions = street_tree.getroot().findall(".//Obec[@kod='"+region_town[Town.code]+"']/Geometrie/PosList")
		boundaries = parse_street_lines(town_positions)
		polygon = Polygon(boundaries)
		town_feature = Feature(geometry=polygon, properties={'name': region_town[Town.town_name], 'region': region_town[Town.region_name], 'measured': region_town[Town.measured]}, id=int(region_town[Town.code]))
		towns_collection.append(town_feature)

	return FeatureCollection(collection_title, towns_collection)

def feature_collection_from_areas(values, country_tree, collection_title):
	"""
	Transformation of information about areas into gejson FeatureCollection.
	Method finds location of street, creates Polygon, and Feature with properties which contains Polygon, and adds it into list `towns_collection`.
	From `towns_collection`, it creates FeatureCollection.

	Parameters
	----------
	values : list of lists
		List of information about areas in following format:
		[measured value, code of area, name of area]
	db_tree : xml.etree.cElementTree
		cElementTree of xml database about contry addresses
	collection_title : string
		What name the resulting FeatureCollection should have.

	Returns
	-------
	geojson.FeatureCollection
		FeatureCollection containing Polygons made from information about areas from `values`.
	"""
	areas_collection = []
	sorted_values = sorted(values, key=lambda area: area[Area.measured])
	for area in values:
		area_positions = country_tree.getroot().findall(".//Okres[@kod='"+area[Area.code]+"']/Geometrie/PosList")
		boundaries = parse_street_lines(area_positions)
		color = get_color(area[Area.measured], sorted_values[0][Area.measured], sorted_values[len(sorted_values)-1][Area.measured])
		polygon = Polygon(boundaries)
		style = {'fill': 'rgba(' + str(color)+ ', 0, 0, 0.8)'}
		properties = {'name': area[Area.area_name], 'measured': area[Area.measured], 'style': style}

		area_feature = Feature(geometry=polygon, properties=properties, id=int(area[Area.code]))
		areas_collection.append(area_feature)

	return FeatureCollection(collection_title, areas_collection)
