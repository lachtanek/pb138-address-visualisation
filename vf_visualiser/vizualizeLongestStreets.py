#!/usr/bin/python
from xml.etree import cElementTree
from xml.etree.ElementTree import Element



class LongestStreetsVizualizer(object):
    tree = None

    def __init__(self):
        self.tree = cElementTree.ElementTree(file="simplified_stat.xml")
    """
    Produces list of tuples (count of address numbers in the street, code of the street)
    one longest street per region
    """    
    def longest_streets(self):
        kraje = self.tree.findall(".//Kraj/@kod")
        maxValues = list(len(kraje))
        i = 0
        for kraj in kraje:
            maximum = (0,0)
            if type(kraj) == Element.__class__ and kraj.tag == "Kraj":
                okresy = self.tree.findall(".//Okres[@kraj = '"+kraj.attrib["kod"]+"']/@kod")

                for okres in okresy:
                    if type(okres) == Element.__class__ and okres.tag == "Okres":
                        dotaz = ".//Obec[@okres='"+okres.attrib["kod"]+"']/@kod"
                        obce = self.tree.findall(dotaz)
                        for obec in obce:
                            if type(obec) == Element.__class__ and obec.tag == "Obec":
                                dotaz = ".//Ulice[@obec='"+obec.attrib["kod"]+"' and @pocetAdresnichMist > "+maximum[0]+"]"       
                                ulice_xml = cElementTree.ElementTree(file="simplified_obec.xml")
                                ulice_obec = ulice_xml.findall(dotaz)
                                for ulice in ulice_obec:
                                    if type(ulice) == Element.__class__ and ulice.tag == "Ulice":
                                        if maximum < ulice.attrib["pocetAdresnichMist"]:
                                            maximum = ulice.attrib["pocetAdresnichMist"], ulice.attrib["kod"]
            maxValues[i] = maximum
            i = i + 1
        return maxValues
    
    
    
    """
    Generates HTML file which vizualizes longest streets
    """
    def generate_html_longest_streets(self):       
                
        root = cElementTree.Element("html")
        header = cElementTree.SubElement(root,"head")
        cElementTree.SubElement(header,"style").text = """
        #map {
            width: 500px;
            height: 400px;
        }"""
        cElementTree.SubElement(header,"title").text = "Longest streets in the Czech Republic regions"
        body = cElementTree.SubElement(root,"body")
        cElementTree.SubElement(body,"h1").text = "Longest streets in the Czech Republic regions"
        cElementTree.SubElement(body,"script").text = """
            var map;
            function initMap() {
                map = new google.maps.Map(document.getElementById('map'), {
                    center: {lat: 49.707572, lng: 15.379676},
                    scrollwheel: true,
                    zoom: 4
                });
            }
            """
        cElementTree.SubElement(body,"div",id = "map")
        cElementTree.SubElement(body,"script src='https://maps.googleapis.com/maps/api/js?callback=initMap' async defer")
        newDoc = cElementTree.ElementTree(root)
        newDoc.write("longestStreets.html", "unicode","html")
        
if __name__ == '__main__':
        vizualizer = LongestStreetsVizualizer()
        vizualizer.generate_html_longest_streets()   