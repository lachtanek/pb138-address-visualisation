#!/usr/bin/python
from xml.etree import cElementTree





class LongestStreetsVisualiser(object):
    stat_filepath = None
    obec_filepath = None
    
    def __init__(self, stat_filepath, ulice_filepath):
        self.stat_filepath = stat_filepath
        self.obec_filepath = ulice_filepath
        
        
        
    """
    Produces list of lists:
    [count of address numbers in the street, code of the street, name of the street, name of the town, name of the region]
    one longest street per region
    """    
    def find(self):
        tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
        kraje = tree_stat.findall(".//Kraj/@kod")
        maxValues = list(len(kraje))
        i = 0
        for kraj in kraje:
            maximum = [0,None,None,None,None]
            if type(kraj) == cElementTree.Element.__class__ and kraj.tag == "Kraj":
                okresy = tree_stat.findall(".//Okres[@kraj = '"+kraj.attrib["kod"]+"']/@kod")

                for okres in okresy:
                    if type(okres) == cElementTree.Element.__class__ and okres.tag == "Okres":
                        dotaz = ".//Obec[@okres='"+okres.attrib["kod"]+"']/@kod"
                        obce = tree_stat.findall(dotaz)
                        for obec in obce:
                            if type(obec) == cElementTree.Element.__class__ and obec.tag == "Obec":
                                dotaz = ".//Ulice[@obec='"+obec.attrib["kod"]+"' and @pocetAdresnichMist > "+maximum[0]+"]"       
                                ulice_xml = cElementTree.ElementTree(file=self.ulice_filepath)
                                ulice_obec = ulice_xml.findall(dotaz)
                                for ulice in ulice_obec:
                                    if type(ulice) == cElementTree.Element.__class__ and ulice.tag == "Ulice":
                                        if maximum[0] < ulice.get("pocetAdresnichMist"):
                                            maximum = [ulice.find("pocetAdresnichMist"), ulice.get("kod"), ulice.find("nazev").text, obec.find("nazev").text, kraj.find("nazev").text]
            maxValues[i] = maximum
            i = i + 1
        return maxValues
    
