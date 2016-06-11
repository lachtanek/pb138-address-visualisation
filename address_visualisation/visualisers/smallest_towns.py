#!/usr/bin/python3
from sys import maxsize
from address_visualisation import Visualiser
from address_visualisation.transformToFeatureCollection import feature_collection_from_towns

class SmallestTownsVisualiser(Visualiser):
    """
    Visualiser which finds towns with least address places in database xml and turns information about them into geojson format.

    ...
    Methods
    -------
    find()
        Finds towns with most address places in region and returns information about them in list of lists.
    run()
        Calls find method and turns its result to geojson FeatureCollection.
    """
    def find(self):
        """
        Finds towns with least address places in each region in xml tree and returns information about its location.

        For each region, it searches through xml tree for towns in region and checks their number of address places.
        If this number is less than minimum of region, method saves information about it into `min_values` on the position of region.

        Returns
        -------
        type
            list of lists

        min_values : list of lists
            For each region one array with following information about smallest town in region:
            [number of address places, code of town, name of town, name of region]

        """
        root = self.db_tree.getroot()

        kraje = root.findall(".//Kraj")
        min_values = {kraj.get("kod"): (maxsize, None, None, kraj.find("Nazev").text) for kraj in kraje}

        obce = {
            obec.get("kod"): (
                int(obec.find("PocetAdresnichMist").text) if obec.find("PocetAdresnichMist") else 0,
                obec.find("Nazev").text,
                obec.get("okres")[0:2]
            ) for obec in root.iter('Obec')
        }

        for ulice in root.iter("Ulice"):
            kod_obce = ulice.get("obec")
            pocet_adresnich_mist = int(ulice.find("PocetAdresnichMist").text)
            obce[kod_obce] = (obce[kod_obce][0] + pocet_adresnich_mist, obce[kod_obce][1], obce[kod_obce][2])

        for kod_obce, obec in obce.items():
            pocet_adresnich_mist = obec[0]
            nazev_obce = obec[1]
            kod_kraje = obec[2]
            if pocet_adresnich_mist < min_values[kod_kraje][0]:
                nazev_kraje = min_values[kod_kraje][3]
                min_values[kod_kraje] = (pocet_adresnich_mist, kod_obce, nazev_obce, nazev_kraje)

        return list(min_values.values())

    def run(self):
        """
        Runs visualiser - gets information about smallest towns and converts it into geojson FeatureCollection.

        Calls find method for getting required information in list of lists and converts it into geojson FeatureCollection.

        Returns
        -------
        geojson.FeatureCollection
            FeatureCollection containing Polygons of smallest towns
        """
        data = self.find()
        return feature_collection_from_towns(data, self.db_tree, 'Smallest towns in region')
