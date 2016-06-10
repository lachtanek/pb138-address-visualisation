"""Downloader."""

import os
import queue

from collections import namedtuple
from datetime import date
import logging
from re import compile
from sys import stderr
from tempfile import TemporaryDirectory
from threading import Thread
from time import sleep

from .helpers import download_file, uncompress


class Downloader:
	"""Used for download and uncompress of files in "RUIAN Vymenny Format" format.

	If you don't use temp_dir and end the application when the download isn't finished, everything is lost.
	"""

	URL_FNAME_RE = compile(r'(\w+\.xml)\.gz')
	FNAME_VERSION_RE = compile(r'(\d+?)_([^_]+?)_(?:(\d+)_)?.*')

	SUBDIR_NAME = 'download'
	STAT_NAME = 'stat'

	def __init__(self, link_file, temp_directory=None, max_threads=2):
		"""Class constructor.

		Parameters
		----------
		link_file : string
			Path to file containing xml-archive links (from http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej)
		temp_directory : string
			Path to working directory, if you wish to use custom ("permanent") temporary directory
		max_threads : int
			Number of concurrent threads for download and transformation of files
		"""
		self._link_file = link_file
		self._file_queue = queue.Queue()
		self._threads = []
		self._running = True
		self._done = False
		self.max_threads = max_threads

		if temp_directory is not None:
			self.temp_directory = temp_directory
			if not os.path.exists(self.temp_directory):
				os.makedirs(self.temp_directory, exist_ok=True)
		else:
			self._obj_temp_directory = TemporaryDirectory()
			self.temp_directory = self._obj_temp_directory.name

		os.makedirs(self.temp_directory + '/' + Downloader.SUBDIR_NAME, exist_ok=True)

	def _isdone(self, outfile):
		if outfile is None:  # stat
			return os.path.exists(self.temp_directory + '/' + Downloader.STAT_NAME + '.full.xml')
		else:
			return os.path.exists(self.temp_directory + '/' + Downloader.SUBDIR_NAME + '/' + outfile)

	def _thread_process_queue(self, threadId):
		while self._running:
			data = self._file_queue.get()
			if data is None:
				break

			if data[1] is None:
				fname2 = self.temp_directory + '/' + Downloader.STAT_NAME + '.full.xml'
			else:
				fname2 = self.temp_directory + '/' + Downloader.SUBDIR_NAME + '/' + data[1]
			fname1 = fname2 + '.gz'

			try:
				download_file(data[0], fname1)
				uncompress(fname1, fname2)

				logging.debug('Done %s', data[1])
			except Exception as e:
				logging.error('Failed %s, error: %s', data[1], str(e))
			finally:
				self._file_queue.task_done()
				if os.path.isfile(fname1):
					os.unlink(fname1)

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
					outfname = None
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
			t = Thread(target=self._thread_process_queue, args=(i,))
			t.start()
			self._threads.append(t)

		filling.join()

		# self._file_queue.join()
		# not using join because it blocks and doesn't support timeout and
		# KeyboardInterrupt is ignored or something (we want to be able to stop and resume the program)
		while not self._file_queue.empty():
			sleep(100)

		logging.debug('All threads finished')

		for i in range(self.max_threads):
			self._file_queue.put(None)
		for t in self._threads:
			t.join()

		if self._running:
			self._done = True

	def download(self):
		"""Start the downloading and uncompressing of XML files.

		Can take up to 3 hours with 5 threads using up to 2GB RAM at peaks.
		"""
		print('Downloading and parsing XML files (this will take long time, depending on number of threads)')
		if len(os.listdir(self.temp_directory + '/' + Downloader.SUBDIR_NAME)) > 0:
			print('Temp directory contains some files, resuming...')

		try:
			self._main_thread()
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
