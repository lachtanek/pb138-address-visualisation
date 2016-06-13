"""Parser."""

import logging
import os
from queue import Queue

from glob import glob
from shutil import move, rmtree
from subprocess import call
from xml.etree import ElementTree

from .downloader import Downloader


class SaxonParser:
	"""Used for XSLT transformation of files in "RUIAN Vymenny Format" format."""

	SUBDIR_NAME = 'parser'

	def __init__(
		self, output, xsl_stat='vf_resources/simplify_stat.xsl', xsl_obec='vf_resources/simplify_obec.xsl',
		saxon_max_threads=2, saxon_path='saxon9he.jar'
	):
		"""Class constructor.

		Parameters
		----------
		xsl_stat : string
			Path to "stat" XSL transformation.
		xsl_obec : string
			Path to "obec" XSL transformation.
		saxon_max_threads : int
			RAM allowed is saxon_max_threads * 1.
		saxon_path : string
		"""
		self._downloader = None
		self._xsl_stat = xsl_stat
		self._xsl_obec = xsl_obec
		self._output_file = output
		self._done = False
		self.queue = Queue()
		self.saxon_max_threads = saxon_max_threads
		self.saxon_path = saxon_path
		self.saxon_max_ram = saxon_max_threads  # * 1

	def _after_attach(self):
		d = self._downloader.temp_directory + '/' + SaxonParser.SUBDIR_NAME
		rmtree(d, ignore_errors=True)
		os.makedirs(d)

	def _run_saxon(self, saxon_in, saxon_out=None):
		xsl = self._xsl_stat
		if saxon_out is None:
			saxon_out = ''
			xsl = self._xsl_obec

		call([
			'java', '-Xmx' + str(self.saxon_max_ram) + 'G', '-cp', self.saxon_path, 'net.sf.saxon.Transform',
			'-threads:' + str(self.saxon_max_threads),
			'-s:' + saxon_in,
			'-xsl:' + xsl,
			'-o:' + self._downloader.temp_directory + '/' + saxon_out,
			'-versionmsg:off', '-warnings:' + 'recover' if logging.root.level <= logging.DEBUG else 'silent'
		])

	def run(self):
		"""Start the process of transforming XML files.

		Takes about 20 minutes with 6 threads and 6GB RAM at peaks.
		"""
		while self._downloader._running:
			data = self.queue.get()
			if data is None:
				break

			logging.debug('Running saxon...')

			arg1 = data[0]
			if isinstance(data[0], list):
				for f in data[0]:
					move(f, self._downloader.temp_directory + '/' + SaxonParser.SUBDIR_NAME)

				arg1 = self._downloader.temp_directory + '/' + SaxonParser.SUBDIR_NAME

			self._run_saxon(arg1, data[1])

			for f in glob(self._downloader.temp_directory + '/' + SaxonParser.SUBDIR_NAME + '/*'):
				os.unlink(f)

			self.queue.task_done()

	def merge(self, delete_temp=True):
		"""Merge."""
		xml_files = glob(self._downloader.temp_directory + '/*.xml')
		xml_element_tree = ElementTree.parse(self._downloader.temp_directory + '/' + Downloader.STAT_NAME + '.xml')
		insertion_point = xml_element_tree.find("./Data")

		for xml_file in xml_files:
			if Downloader.STAT_NAME in xml_file:
				continue

			data = ElementTree.parse(xml_file).getroot()
			result = data.find('./Data')
			mista = result.find('./AdresniMista')

			if mista:
				result.remove(mista)
				kodObec = mista.get('obec')
				if kodObec:
					obec = insertion_point.find('./Obce/Obec[@kod="' + kodObec + '"]')
					obec.append(mista.find('PocetAdresnichMist'))
					continue

			insertion_point.extend(result)

		if xml_element_tree is not None:
			xml_element_tree.write(self._output_file, encoding='utf-8')
			logging.debug('Files merged into ' + self._output_file)

			if delete_temp:
				rmtree(self._downloader.temp_directory)
