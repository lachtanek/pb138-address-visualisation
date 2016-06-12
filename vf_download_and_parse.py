#!/usr/bin/python3
"""Neco."""
import logging
from address_visualisation import Downloader, SaxonParser

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

par = SaxonParser('vf_resources/db.xml', saxon_max_threads=2)
dow = Downloader(par, 'vf_resources/links.txt', temp_directory='vf_resources/tmp', max_threads=2)
dow.run()
par.merge()
