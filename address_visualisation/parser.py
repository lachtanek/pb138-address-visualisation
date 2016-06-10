"""Parser."""

from glob import glob
import logging
from shutil import rmtree
from subprocess import call
from xml.etree import ElementTree

from .downloader import Downloader


class SaxonParser:
	"""Used for XSLT transformation of files in "RUIAN Vymenny Format" format."""

	def __init__(
		self, downloader, output, xsl_stat='vf_simplify/simplify_stat.xsl', xsl_obec='vf_simplify/simplify_obec.xsl',
		saxon_max_threads=2, saxon_path='saxon9he.jar', saxon_max_ram=2
	):
		"""Class constructor."""
		self._downloader = downloader
		self._xsl_stat = xsl_stat
		self._xsl_obec = xsl_obec
		self._output_file = output
		self._running = True
		self._done = False
		self.saxon_max_threads = saxon_max_threads
		self.saxon_path = saxon_path
		self.saxon_max_ram = saxon_max_ram

	def run(self):
		"""Start the process of transforming XML files."""
		call([
			'java', '-Xmx' + str(self.saxon_max_ram) + 'G', '-cp', self.saxon_path, 'net.sf.saxon.Transform',
			'-threads:' + str(self.saxon_max_threads),
			'-s:' + self._downloader.temp_directory + '/' + Downloader.SUBDIR_NAME,
			'-xsl:' + self._xsl_obec,
			'-o:' + self._downloader.temp_directory,
			'-versionmsg:off', '-warnings:' + 'recover' if logging.root.level <= logging.DEBUG else 'silent'
		])

		call([
			'java', '-Xmx' + str(self.saxon_max_ram) + 'G', '-cp', self.saxon_path, 'net.sf.saxon.Transform',
			'-s:' + self._downloader.temp_directory + '/' + Downloader.STAT_NAME + '.full.xml',
			'-xsl:' + self._xsl_stat,
			'-o:' + self._downloader.temp_directory + '/' + Downloader.STAT_NAME + '.xml',
			'-versionmsg:off', '-warnings:' + 'recover' if logging.root.level <= logging.DEBUG else 'silent'
		])

	def merge(self):
		xml_files = glob(self._downloader.temp_directory + '/*.xml')
		xml_element_tree = None

		for xml_file in xml_files:
			data = ElementTree.parse(xml_file).getroot()

			for result in data.iter('Data'):
				if xml_element_tree is None:
					xml_element_tree = data
					insertion_point = xml_element_tree.findall("./Data")[0]
				else:
					insertion_point.extend(result)

		if xml_element_tree is not None:
			tree = ElementTree.ElementTree(xml_element_tree)
			tree.write(self._output_file, encoding='utf-8')
			logging.debug('Files merged into ' + self._output_file)

			rmtree(self._downloader.temp_directory)
