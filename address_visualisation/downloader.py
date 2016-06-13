"""Downloader."""

import logging
import os
import queue

from collections import namedtuple
from datetime import date
from re import compile
from shutil import rmtree
from sys import stderr
from tempfile import TemporaryDirectory
from threading import Thread, Lock
from time import sleep

from .helpers import download_file, uncompress


class Downloader:
	"""Used for download and uncompress of files in "RUIAN Vymenny Format" format.

	If you don't use temp_dir and end the application when the download isn't finished, everything is lost.
	"""

	URL_FNAME_RE = compile(r'(\w+\.xml)\.gz')
	FNAME_VERSION_RE = compile(r'(\d+?)_([^_]+?)_(?:(\d+)_)?.*')

	SUBDIR_NAME = 'download'
	STATE_FILE_NAME = 'stat'

	def __init__(self, parser, link_file, temp_directory=None, max_threads=2, max_download_size_mb=1024):
		"""When you run Downloader, it runs Parser, too.

		For maximum performance of Downloader you need to find good balance between max_threads, max_download_size_mb and
		Parser's max_threads, taking into account your connection speed and processor speed (and available RAM).

		Parameters
		----------
		link_file : string
			Path to file containing xml-archive links (from http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej).
		temp_directory : string
			Path to working directory, if you wish to use custom ("permanent") temporary directory.
		max_threads : int
			Number of concurrent threads for downloading of files.
		max_download_size_mb : int
			When this limit is reached, parser starts to work.
		"""
		self._parser = parser
		parser._downloader = self
		self._link_file = link_file
		self._file_queue = queue.Queue()
		self._threads = []
		self._running = True
		self.max_threads = max_threads
		self._current_size = 0
		self._current_files = []
		self._current_lock = Lock()
		self.max_download_size_mb = max_download_size_mb

		if temp_directory is not None:
			self.temp_directory = temp_directory
			if not os.path.exists(self.temp_directory):
				os.makedirs(self.temp_directory, exist_ok=True)
		else:
			self._obj_temp_directory = TemporaryDirectory()
			self.temp_directory = self._obj_temp_directory.name

		self._parser._after_attach()

		d = self.temp_directory + '/' + Downloader.SUBDIR_NAME
		rmtree(d, ignore_errors=True)
		os.makedirs(d)

	def _isdone(self, outfile):
		if outfile is None:  # stat
			return os.path.exists(self.temp_directory + '/' + Downloader.STATE_FILE_NAME + '.full.xml')
		else:
			return os.path.exists(self.temp_directory + '/' + Downloader.SUBDIR_NAME + '/' + outfile)

	def _check_size(self, fname, force=False):
		if fname is not None:
			self._current_size += os.path.getsize(fname) / (1024 ** 2)
			self._current_files.append(fname)

		if force or self._current_size > self.max_download_size_mb:
			logging.debug('Waking parser')

			if len(self._current_files) > 0:
				self._parser.queue.put((self._current_files[:], None))

			self._current_size = 0
			self._current_files = []

	def _thread_process_queue(self, threadId):
		while self._running:
			data = self._file_queue.get()
			if data is None:
				break

			if data[1] is None:
				fname2 = self.temp_directory + '/' + Downloader.STATE_FILE_NAME + '.full.xml'
				isState = True
			else:
				fname2 = self.temp_directory + '/' + Downloader.SUBDIR_NAME + '/' + data[1]
				isState = False
			fname1 = fname2 + '.gz'

			try:
				download_file(data[0], fname1)
				uncompress(fname1, fname2)

				if not isState:
					with self._current_lock:
						self._check_size(fname2)

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
		self._parser_thread = Thread(target=self._parser.run)
		self._parser_thread.start()
		self._filling_thread = Thread(target=self._thread_fill_queue)
		self._filling_thread.start()

		for i in range(self.max_threads):
			t = Thread(target=self._thread_process_queue, args=(i,))
			t.start()
			self._threads.append(t)

		self._filling_thread.join()

		# self._file_queue.join()
		# not using join because it blocks and doesn't support timeout and
		# KeyboardInterrupt is ignored or something (we want to be able to stop and resume the program)
		while not self._file_queue.empty():
			sleep(100)

		logging.debug('All threads finished')
		with self._current_lock:
			self._check_size(None, True)

		for i in range(self.max_threads):
			self._file_queue.put(None)
		for t in self._threads:
			t.join()

		self._parser.queue.put((self.temp_directory + '/' + Downloader.STATE_FILE_NAME + '.full.xml', Downloader.STATE_FILE_NAME + '.xml'))
		self._parser.queue.put(None)

		self._parser_thread.join()

		logging.debug('Parser finished')

	def run(self):
		"""Start downloading and uncompressing XML files and run Parser.

		Raises
		------
		KeyboardInterrupt
			Stops working threads and re-raises exception.
		"""
		print('Downloading and parsing XML files (this will take long time, depending on number of threads)')
		if len(os.listdir(self.temp_directory + '/' + Downloader.SUBDIR_NAME)) > 0:
			print('Temp directory contains some files, resuming...')

		try:
			self._main_thread()
		except KeyboardInterrupt:
			print('Stopping download (can take a few seconds to stop working threads)')
			self._running = False
			if self._filling_thread.is_alive():
				self._filling_thread.join()
			if self._parser_thread.is_alive():
				self._parser.queue.put(None)
				self._parser_thread.join()

			if not self._file_queue.empty():
				with self._file_queue.mutex:
					self._file_queue.queue.clear()

				for i in range(self.max_threads):
					self._file_queue.put(None)
				for t in self._threads:
					if t.is_alive():
						t.join()

			raise  # re-raise KeyboartInterrupt
