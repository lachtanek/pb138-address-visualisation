#!/usr/bin/python3

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
        tree_ulice = cElementTree.ElementTree(file=self.obec_filepath)
        root = tree_stat.getroot()

        kraje = root.findall(".//Kraj")
        max_values = {kraj.get("kod"): (0, None, None, None, kraj.find("Nazev").text) for kraj in kraje}

        obce = {obec.get("kod"): (obec.find("Nazev").text, obec.get("okres")[0:2]) for obec in root.iter('Obec')}

        for ulice in tree_ulice.getroot().iter('Ulice'):
            pocet_adresnich_mist = int(ulice.find("PocetAdresnichMist").text)
            kod_obce = ulice.get("obec")
            kod_kraje = obce[kod_obce][1]
            nazev_obce = obce[kod_obce][0]

            if pocet_adresnich_mist > max_values[kod_kraje][0]:
                max_values[kod_kraje] = (pocet_adresnich_mist, ulice.get("kod"), ulice.find("Nazev").text, nazev_obce, max_values[kod_kraje][4])

        return list(max_values.values())
"""
if __name__ == '__main__':
    visualiser = LongestStreetsVisualiser("simplified_stat.xml","simplified_obec_kompletni.xml")
    values = visualiser.find()
    print(values)
"""
