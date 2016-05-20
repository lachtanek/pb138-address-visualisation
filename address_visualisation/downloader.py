import os
import queue

from collections import namedtuple
from datetime import date
from glob import glob
from lxml import etree
from subprocess import call
from sys import stderr
from tempfile import TemporaryDirectory
from threading import Thread
from time import sleep
from xml.etree import ElementTree

from .base import Settings
from .helpers import download_file, uncompress


class Downloader:
	def __init__(self, link_file, output, xsl, temp_dir=None):
		self.link_file = link_file
		self.xsl = xsl
		self.output_file = output
		self.file_queue = queue.Queue()
		self.big_file_queue = queue.Queue()
		self.threads = []
		self.running = True

		if temp_dir is not None:
			self.temp_directory = temp_dir
			if not os.path.exists(self.temp_directory):
				os.makedirs(self.temp_directory)
		else:
			self.temp_directory_obj = TemporaryDirectory()
			self.temp_directory = self.temp_directory_obj.name


	def isdone(self, outfile):
		return os.path.exists(self.temp_directory + '/' + outfile)


	def thread_process_queue(self):
		while self.running:
			data = self.file_queue.get()
			if data is None:
				break

			fname1 = fname2 = None
			skipped = False

			try:
				fname1 = download_file(data[0])

				if os.path.getsize(fname1) > Settings.BIGFILE_MIN_ARCHIVE_MB * 1024 * 1024: # bigger than 10MB -> leave it for later
					self.big_file_queue.put((fname1, data[1]))
					skipped = True

					if Settings.DEBUG:
						print('skipping ' + data[1] + ' (' + fname1 + ') for now, because it\'s too big')

					continue

				fname2 = uncompress(fname1)

				self.transform(fname2, data[1])

				if Settings.DEBUG:
					print('done', data[1])
			except (MemoryError, etree.XSLTApplyError) as e:
				if Settings.DEBUG:
					print('failed', data[1], 'error:', str(e), file=stderr)
			except Exception as e:
				print('failed', data[1], 'error:', str(e), file=stderr)
			finally:
				self.file_queue.task_done()
				if not skipped and fname1:
					os.unlink(fname1)
				if fname2:
					os.unlink(fname2)


	def thread_fill_queue(self):
		FileData = namedtuple('FileData', ['date', 'downlink', 'outfile'])
		uniq = {}

		with open(self.link_file, 'r') as linkList:
			for line in linkList:
				m = Settings.URL_FNAME_RE.search(line)
				if not m:
					continue

				fname = m.group(1)
				m = Settings.FNAME_VERSION_RE.search(fname)
				if not m:
					continue

				datestr = m.group(1)
				file_date = date( int( datestr[:4] ), int( datestr[4:6] ), int( datestr[6:] ) )
				townid = int(m.group(2))

				if townid in uniq and uniq[townid].date >= file_date:
					continue

				uniq[townid] = FileData(file_date, line, str(townid) + '.xml')

		for data in uniq.values():
			if not self.isdone(data.outfile):
				self.file_queue.put((data.downlink, data.outfile))


	def main_thread(self):
		filling = Thread(target=self.thread_fill_queue)
		filling.start()

		for i in range(Settings.MAX_THREADS):
			t = Thread(target=self.thread_process_queue)
			t.start()
			self.threads.append(t)

		filling.join()

		# self.file_queue.join()
		# not using join because it blocks and doesn't support timeout and
		# KeyboardInterrupt is ignored or something (we want to be able to stop program!)
		while not self.file_queue.empty():
			sleep(100)

		if Settings.DEBUG:
			print('joined queue')

		for i in range(Settings.MAX_THREADS):
			self.file_queue.put(None)
		for t in self.threads:
			t.join()

		fname2 = None

		while self.running:
			try:
				data = self.big_file_queue.get(False)
				if not data:
					break
			except queue.Empty:
				break

			try:
				fname2 = uncompress(data[0])
				call( [ 'java', '-Xmx' + Settings.SAXON_MAX_RAM + 'G', '-cp', Settings.SAXON_PATH,
						'net.sf.saxon.Transform', '-s:' + fname2, '-xsl:' + self.xsl, '-o:' + self.temp_directory + '/' + data[1] ] )

				if Settings.DEBUG:
					print('done', data[1])
			except etree.XSLTApplyError as e:
				if Settings.DEBUG:
					print('failed', data[1], 'error:', str(e), file=stderr)
			except Exception as e:
				print('failed', data[1], 'error:', str(e), file=stderr)
			finally:
				self.big_file_queue.task_done()
				os.unlink(data[0])
				if fname2:
					os.unlink(fname2)


	def download_and_parse(self):
		print( 'Downloading and parsing XML files (this might take a long time, like 30 minutes)' )

		try:
			self.main_thread()
		except KeyboardInterrupt:
			print('Stopping download (give it a few seconds...)')
			self.running = False

			if not self.file_queue.empty():
				with self.file_queue.mutex:
					self.file_queue.queue.clear()

				for i in range(Settings.MAX_THREADS):
					self.file_queue.put(None)
				for t in self.threads:
					t.join()

			raise


	def merge(self):
		xml_files = glob(self.temp_directory + '/*.xml')
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
			tree.write( self.output_file, encoding='utf-8' )
			if Settings.DEBUG:
				print( 'Files merged into ' + self.output_file )


	def transform(self, inputFile, outputFile):
		xml = etree.parse(inputFile)
		xslt = etree.parse(self.xsl)
		doTransform = etree.XSLT(xslt)
		newdom = doTransform(xml)
		with open(self.temp_directory + '/' + outputFile, 'wb') as wr:
			wr.write( etree.tostring(newdom, pretty_print=True, encoding='utf-8') )
