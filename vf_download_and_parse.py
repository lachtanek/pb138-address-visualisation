#!/usr/bin/python3
from vf_parser import VF
pars = VF('vf_resources/links_obec.txt', 'vf_resources/tmp', 'vf_simplify/simplify_obec.xsl')
pars.download_and_parse()
