from xml.etree import cElementTree
from geojson import Feature, MultiLineString, Point, Polygon
from features import FeatureCollection
from helpers import multi_segment_length, parse_street_lines, parse_segment

class Street():
    measured = 0
    code = 1
    street_name = 2
    town_name = 3
    region_name = 4

class Town():
    measured = 0
    code = 1
    town_name = 2
    region_name = 3

class Area():
    measured = 0
    code = 1
    area_name = 2

"""
Generates GEOJSON FeatureCollection which vizualizes given streets
"""
def feature_collection_from_streets(values, street_filepath, collection_title):
    tree = cElementTree.ElementTree(file=street_filepath)
    streets_collection = []
    for region_street in values:
        street_positions = tree.getroot().findall(".//Ulice[@kod='"+region_street[1]+"']/Geometrie/PosList")
        lines = parse_street_lines(street_positions)

        mls = MultiLineString(lines)
        length = multi_segment_length(lines)
        street_feature = Feature(geometry=mls, properties={'name': region_street[Street.street_name], 'town': region_street[Street.town_name], 'region': region_street[Street.region_name], 'length': length, 'measured': region_street[Street.measured]}, id=int(region_street[Street.code]))
        streets_collection.append(street_feature)

    return FeatureCollection(collection_title, streets_collection)

def feature_collection_from_towns(values, street_filepath, collection_title):
    tree = cElementTree.ElementTree(file=street_filepath)
    towns_collection = []
    for region_town in values:
        town_streets = tree.getroot().findall(".//Ulice[@obec='"+region_town[Town.code]+"']")
        street_positions = town_streets[len(town_streets)//2].findall("./Geometrie/PosList")
        lines = parse_street_lines(street_positions)

        middle_line = lines[len(lines)//2]
        middle_point = Point(middle_line[len(middle_line)//2])
        town_feature = Feature(geometry=middle_point, properties={'name': region_town[Town.town_name], 'region': region_town[Town.region_name], 'measured': region_town[Town.measured]}, id=int(region_town[Town.code]))
        towns_collection.append(town_feature)

    return FeatureCollection(collection_title, towns_collection)

def feature_collection_from_areas(values, country_filepath, collection_title):
    tree = cElementTree.ElementTree(file=country_filepath)
    areas_collection = []
    for area in values:
        area_positions = tree.getroot().find(".//Okres[@kod='"+area[Area.code]+"']/Geometrie/PosList")
        line = parse_segment(area_positions)
        polygon = Polygon(line)
        area_feature = Feature(geometry=polygon, properties={'name': area[Area.area_name], 'measured': area[Area.measured]}, id= int(area[Area.code]))
        areas_collection.append(area_feature)
    return FeatureCollection(collection_title, areas_collection)
        
