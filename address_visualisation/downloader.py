"""Downloader."""

import os
import queue

from collections import namedtuple
from datetime import date
from glob import glob
from lxml import etree
from re import compile
from subprocess import call
from sys import stderr
from tempfile import TemporaryDirectory
from threading import Thread
from time import sleep
from xml.etree import ElementTree

from .helpers import download_file, uncompress


class Downloader:
	"""Used for download and transformation of files in "RUIAN Vymenny Format" format.

	Method download_and_parse() can take about 3 hours to finish with 5 threads and use up to 2GB of RAM,
	so it is advised to use constructor's temp_dir parameter, so you can quit the download and resume it later.
	If you don't use temp_dir, when you end the application and the download isn't finished, everything is lost.
	"""

	URL_FNAME_RE = compile(r'(\w+\.xml)\.gz')
	FNAME_VERSION_RE = compile(r'(\d+?)_([^_]+?)_(?:(\d+)_)?.*')

	DEBUG = False

	def __init__(
		self, link_file, output, xsl_stat='vf_simplify/simplify_stat.xsl', xsl_obec='vf_simplify/simplify_obec.xsl', temp_dir=None, max_threads=2,
		bigfile_archive_min_mb=10, saxon_path='saxon9he.jar', saxon_max_ram=8
	):
		"""Class constructor.

		Parameters
		----------
		link_file : string
			Path to file containing xml-archive links (from http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej)
		output : string
			Path to final XML output file
		xsl : string
			Path to XSL file used to transform XMLs
		temp_dir : string
			Path to directory, if you wish to use custom ("permanent") temporary directory
		max_threads : int
			Number of concurrent threads for download and transformation of files
		bigfile_archive_min_mb : int
			How big an xml-archive must be to use saxon for it's transformation
		saxon_path : string
			Path to Saxon
		saxon_max_ram : int
			Maximum Saxon RAM (in gigabytes)
		"""
		self._link_file = link_file
		self._xsl_stat = xsl_stat
		self._xsl_obec = xsl_obec
		self._output_file = output
		self._file_queue = queue.Queue()
		self._big_file_queue = queue.Queue()
		self._threads = []
		self._running = True
		self._done = False
		self.max_threads = max_threads
		self.bigfile_archive_min_mb = bigfile_archive_min_mb
		self.saxon_path = saxon_path
		self.saxon_max_ram = saxon_max_ram

		if temp_dir is not None:
			self._temp_directory = temp_dir
			if not os.path.exists(self._temp_directory):
				os.makedirs(self._temp_directory)
		else:
			self._temp_directory_obj = TemporaryDirectory()
			self._temp_directory = self._temp_directory_obj.name

	def _isdone(self, outfile):
		return os.path.exists(self._temp_directory + '/' + outfile)

	def _thread_process_queue(self):
		while self._running:
			data = self._file_queue.get()
			if data is None:
				break

			fname1 = fname2 = None
			skipped = False

			try:
				fname1 = download_file(data[0])

				# bigger than 10MB -> leave it for later
				if os.path.getsize(fname1) > self.bigfile_archive_min_mb * 1024 * 1024:
					self._big_file_queue.put((fname1, data[1]))
					skipped = True

					if Downloader.DEBUG:
						print('skipping ' + data[1] + ' (' + fname1 + ') for now, because it\'s too big')

					continue

				fname2 = uncompress(fname1)

				self._transform(fname2, data[1])

				if Downloader.DEBUG:
					print('done', data[1])
			except (MemoryError, etree.XSLTApplyError) as e:
				if Downloader.DEBUG:
					print('failed', data[1], 'error:', str(e), file=stderr)
			except Exception as e:
				print('failed', data[1], 'error:', str(e), file=stderr)
			finally:
				self._file_queue.task_done()
				if not skipped and fname1:
					os.unlink(fname1)
				if fname2:
					os.unlink(fname2)

	def _thread_fill_queue(self):
		FileData = namedtuple('FileData', ['date', 'downlink', 'outfile'])
		uniq = {}

		with open(self._link_file, 'r') as linkList:
			for line in linkList:
				m = Downloader.URL_FNAME_RE.search(line)
				if not m:
					continue

				fname = m.group(1)
				m = Downloader.FNAME_VERSION_RE.search(fname)
				if not m:
					continue

				datestr = m.group(1)
				file_date = date(int(datestr[:4]), int(datestr[4:6]), int(datestr[6:]))

				if m.group(2) == 'ST':  # stat
					townid = -1
					outfname = 'stat.xml'
				else:
					townid = int(m.group(3))
					outfname = str(townid) + '.xml'

				if townid in uniq and uniq[townid].date >= file_date:
					continue

				uniq[townid] = FileData(file_date, line, outfname)

		for idx, data in uniq.items():
			if not self._isdone(data.outfile):
				self._file_queue.put((data.downlink, data.outfile))

	def _main_thread(self):
		filling = Thread(target=self._thread_fill_queue)
		filling.start()

		for i in range(self.max_threads):
			t = Thread(target=self._thread_process_queue)
			t.start()
			self._threads.append(t)

		filling.join()

		# self._file_queue.join()
		# not using join because it blocks and doesn't support timeout and
		# KeyboardInterrupt is ignored or something (we want to be able to stop and resume the program)
		while not self._file_queue.empty():
			sleep(100)

		if Downloader.DEBUG:
			print('joined queue')

		for i in range(self.max_threads):
			self._file_queue.put(None)
		for t in self._threads:
			t.join()

		fname2 = None

		while self._running:
			try:
				data = self._big_file_queue.get(False)
				if not data:
					break
			except queue.Empty:
				break

			try:
				fname2 = uncompress(data[0])
				call([
					'java', '-Xmx' + self.saxon_max_ram + 'G', '-cp', self.saxon_path,
					'net.sf.saxon.Transform', '-s:' + fname2, '-xsl:' + self._xsl_obec, '-o:' + self._temp_directory + '/' + data[1],
					'-versionmsg:off', '-warnings:' + 'recover' if Downloader.DEBUG else 'silent'
				])

				if Downloader.DEBUG:
					print('done', data[1])
			except etree.XSLTApplyError as e:
				if Downloader.DEBUG:
					print('failed', data[1], 'error:', str(e), file=stderr)
			except Exception as e:
				print('failed', data[1], 'error:', str(e), file=stderr)
			finally:
				self._big_file_queue.task_done()
				os.unlink(data[0])
				if fname2:
					os.unlink(fname2)

		if self._running:
			self._done = True

	def download_and_parse(self):
		"""Start the process of downloading, uncompressing and transforming of XML files.

		Can take up to 3 hours with 5 threads using up to 2GB RAM at peaks.
		"""
		print('Downloading and parsing XML files (this will take long time, depending on number of threads)')
		if len(os.listdir(self._temp_directory)) > 0:
			print('Temp directory contains some files, resuming...')

		try:
			self._main_thread()
			if self._done:
				self._merge()
		except KeyboardInterrupt:
			print('Stopping download (can take a few seconds to stop working threads)')
			self._running = False

			if not self._file_queue.empty():
				with self._file_queue.mutex:
					self._file_queue.queue.clear()

				for i in range(self.max_threads):
					self._file_queue.put(None)
				for t in self._threads:
					t.join()

			raise  # re-raise KeyboartInterrupt

	def _merge(self):
		xml_files = glob(self._temp_directory + '/*.xml')
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
			if Downloader.DEBUG:
				print('Files merged into ' + self._output_file)

	def _transform(self, inputFile, outputFile):
		xml = etree.parse(inputFile)
		if outputFile == 'stat.xml':
			xslt = etree.parse(self._xsl_stat)
		else:
			xslt = etree.parse(self._xsl_obec)
		doTransform = etree.XSLT(xslt)
		newdom = doTransform(xml)
		with open(self._temp_directory + '/' + outputFile, 'wb') as wr:
			wr.write(etree.tostring(newdom, pretty_print=True, encoding='utf-8'))
