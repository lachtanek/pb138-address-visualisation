#!/usr/bin/python3
"""Neco."""
import logging
from address_visualisation import Downloader, SaxonParser

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

dow = Downloader('vf_resources/links.txt', temp_directory='vf_resources/tmp', max_threads=5)
dow.download()
par = SaxonParser(dow, 'vf_resources/db.xml', saxon_max_threads=5, saxon_max_ram=6)
par.run()
par.merge()
