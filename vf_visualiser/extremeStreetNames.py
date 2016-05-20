from xml.etree import cElementTree
#from geojson import Feature, MultiLineString, dumps
#from features import FeatureCollection
#from builtins import int
from sys import maxsize

class ExtremeStreetNamesVisualiser(object):
    stat_filepath = None
    obec_filepath = None
    
    def __init__(self, stat_filepath, ulice_filepath):
        self.stat_filepath = stat_filepath
        self.obec_filepath = ulice_filepath
        
    def find(self):
        tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
        root = tree_stat.getroot()
        kraje = root.findall(".//Kraj/@kod")
        minValues = []
        maxValues = []
        
        for kraj in kraje:
            minimum = [maxsize,None,None,None,None]
            maximum = [-1,None,None,None,None]
            if type(kraj) == cElementTree.Element.__class__ and kraj.tag == "Kraj":
                okresy = tree_stat.findall(".//Okres[@kraj = '"+kraj.attrib["kod"]+"']/@kod")

                for okres in okresy:
                    if type(okres) == cElementTree.Element.__class__ and okres.tag == "Okres":
                        dotaz = ".//Obec[@okres='"+okres.attrib["kod"]+"']/@kod"
                        obce = tree_stat.findall(dotaz)
                        for obec in obce:
                            if type(obec) == cElementTree.Element.__class__ and obec.tag == "Obec":
                                      
                                ulice_xml = cElementTree.ElementTree(file=self.ulice_filepath)
                                dotaz = ".//Ulice[@obec='"+obec.attrib["kod"]+"]" 
                                ulice_obec = ulice_xml.getroot().findall(dotaz)
                                for ulice in ulice_obec:
                                    if type(ulice) == cElementTree.Element.__class__ and ulice.tag == "Ulice":
                                        nazev = ulice.get("Nazev")
                                        if maximum[0] < len(nazev):
                                            maximum = [len(nazev), ulice.get("kod"), ulice.find("nazev").text, obec.find("nazev").text, kraj.find("nazev").text]
                                        if minimum[0] > len(nazev):
                                            maximum = [len(nazev), ulice.get("kod"), ulice.find("nazev").text, obec.find("nazev").text, kraj.find("nazev").text]
            minValues.append(minimum)
            maxValues.append(maximum)
        return minValues, maxValues    
    
    
    