#!/usr/bin/python3

from xml.etree import cElementTree

class SquareCountVisualiser(object):
    stat_filepath = None
    ulice_filepath = None

    def __init__(self, stat_filepath, ulice_filepath):
        self.stat_filepath = stat_filepath
        self.ulice_filepath = ulice_filepath

    def find(self):
        tree_stat = cElementTree.ElementTree(file=self.stat_filepath)
        tree_ulice = cElementTree.ElementTree(file=self.ulice_filepath)
        root = tree_stat.getroot()
        okresy = root.findall(".//Okres")
        values=[None]*len(okresy)
        i = 0
        for okres in okresy:
            count=[0,okres.get("kod"), okres.find("Nazev").text]
            for obec in root.iter('Obec'):
                if obec.get("okres") == okres.get("kod"):
                    for ulice in tree_ulice.iter('Ulice'):
                        if ulice.get("obec") == obec.get("kod"):
                            nazev = ulice.find("Nazev").text
                            if "nám" in nazev or "Nám" in nazev:
                                count = [count[0]+1, okres.get("kod"), okres.find("Nazev").text]
            values[i] = count
            i = i + 1
        return values
"""
if __name__ == '__main__':
    visualiser = SquareCountVisualiser("simplified_stat.xml","simplified_obec.xml")
    values = visualiser.find()
    print(values)
"""
