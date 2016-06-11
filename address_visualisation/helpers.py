import gzip
from math import sqrt
from urllib import request

BUFF_SIZE = 4096


def download_file(address, target):
	"""
	Downloads file - copies content on url address to target file.
	
	Parameters
	----------
	address : url
		URL address to download from
	target : string
		path to downloaded file
	
	Raises
	------
	Exception
		Download failed.
	"""
	with request.urlopen(address) as sock:
		with open(target, 'wb') as writeF:
			while True:
				data = sock.read(BUFF_SIZE)
				if not data:
					break

				writeF.write(data)

		return

	raise Exception('Failed to download ' + address)


def uncompress(fileName, target):
	"""
	Uncompresses file.
	
	Extracts compressed file on `fileName` filepath to `target` filepath.
	
	Parameters
	----------
	fileName : string
		Path to file to uncompress.
	target : string
		Path to file where uncompressed data should be stored.
		
	Raises
	------
	Exception
		Uncompressing failed.
	"""
	with gzip.open(fileName) as gzf:
		with open(target, 'wb') as writeF:
			while True:
				data = gzf.read(BUFF_SIZE)
				if not data:
					break

				writeF.write(data)

		return

	raise Exception('Failed to uncompress ' + fileName)


def segment_length(seg):
	"""
	Measures length of line represented by list of tuples with coordinates.
	
	Parameters
	----------
	seg : list of tuples of float
		Line represented by list of tuples with coordinates.
	
	Returns
	-------
	length : float
		Length of line.
	"""
	length = 0
	for i in range(1, len(seg)):
		length += sqrt((seg[i - 1][0] - seg[i][0]) ** 2 + (seg[i - 1][1] - seg[i][1]) ** 2)

	return length


def multi_segment_length(segs):
	"""
	Measures length of multiline represented by list of lists of tuples with coordinates.
	
	Parameters
	----------
	segs : list of lists of tuples of float
		Multiline represented by list of lines.
	
	Returns
	-------
	float
		Summary of length of lines in multiline.
	"""
	return sum(map(segment_length, segs))


def parse_segment(seg):
	"""
	Parses line represented by string to list of points(tuples with coordinates).
	
	Parameters
	----------
	seg : string
		String containing coordinates of line, like "0.0 0.0 3.0 3.0"
	
	Returns
	-------
	points : list of tuples of float
		Line as list of tuples with coordinates
	"""
	coords = seg.text.split()
	points = []

	for i in range(0, len(coords), 2):
		points.append((float(coords[i]), float(coords[i + 1])))

	return points


def parse_street_lines(segs):
	"""
	Parses multiline represented by list of strings to list of points(tuples with coordinates).
	
	Parameters
	----------
	segs : list of strings
		Multiline represented by list of lines.
		
	Returns
	-------
	list of list of tuples of float
		Multiline as list of lines(lists of tuples with coordinates)
	"""
	return list(map(parse_segment, segs))

def get_color(measured_value, min_value, max_value):
	"""
	Returns fullness of colour to use in geojson.Feature based on position of measured_value in range of value.
	
	Parameters
	----------
	measured_value : int
		Measured value.
	min_value : int
		Minimal value in range.
	max_value : int
		Maximal value in range.
	
	Returns
	-------
	int
		Fullness of color in range 50 - 250.
	"""
	differ = (max_value - min_value) / 5
	i = 1
	while i*differ <= max_value:
		if measured_value <= (min_value + i*differ):
			return i * 50
		i = i + 1
		
