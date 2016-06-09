#!/usr/bin/python3
from address_visualisation import Downloader
Downloader.DEBUG = True
dow = Downloader(
	'vf_resources/links.txt', 'vf_resources/db.xml', 'vf_simplify/simplify_obec.xsl',
	'vf_resources/tmp', saxon_path='saxon9he.jar', max_threads=5
)
dow.download_and_parse()
