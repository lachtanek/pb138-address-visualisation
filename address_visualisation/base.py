import re

class Settings:
	URL_FNAME_RE = re.compile(r'(\w+\.xml)\.gz')
	FNAME_VERSION_RE = re.compile(r'(\d+?)_[^_]+?_(\d+)_.*')
	# maybe move somewhere else in the future
	BUFF_SIZE = 4096
	MAX_THREADS = 2
	DEBUG = False
	SAXON_PATH = 'saxon9he.jar'
	SAXON_MAX_RAM = '8'
