#!/usr/bin/python3
from address_visualisation import Downloader, Settings
Settings.MAX_THREADS = 5
Settings.DEBUG = True
Settings.SAXON_PATH = 'saxon9he.jar'
dow = Downloader('vf_resources/links_obec_kompletni.txt', 'vf_resources/tmp/', 'vf_simplify/simplify_obec.xsl')
dow.download_and_parse()
dow.merge()
