from xml.etree import cElementTree

class townWithMostStreetsVisualiser(object):
    stat_filepath = None
    ulice_filepath = None
    
    def __init__(self, stat_filepath, ulice_filepath):
        self.stat_filepath = stat_filepath
        self.ulice_filepath = ulice_filepath
        
    def find(self):
        tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
        root = tree_stat.getroot()
        kraje = root.findall(".//Kraj/@kod")
        maxValues = []
        
        for kraj in kraje:
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
                                ulice_obec = ulice_xml.getroot().find(dotaz)
                                if maximum[0] < len(ulice_obec):
                                    maximum = [len(ulice_obec), obec.get("kod"), obec.find("nazev").text, kraj.find("nazev").text]                                      
            maxValues.append(maximum)
        return maxValues    
    
    
    