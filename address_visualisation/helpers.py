import gzip
from math import sqrt
from urllib import request

BUFF_SIZE = 4096


def download_file(address, target):
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
	length = 0
	for i in range(1, len(seg)):
		length += sqrt((seg[i - 1][0] - seg[i][0]) ** 2 + (seg[i - 1][1] - seg[i][1]) ** 2)

	return length


def multi_segment_length(segs):
	return sum(map(segment_length, segs))


def parse_segment(seg):
	coords = seg.text.split()
	points = []

	for i in range(0, len(coords), 2):
		points.append((float(coords[i]), float(coords[i + 1])))

	return points


def parse_street_lines(segs):
	return list(map(parse_segment, segs))

def get_opacity(measured_value, max_value):
	differ = max_value / 5
	i = 1
	while i*differ <= max_value:
		if measured_value <= i*differ:
			return i * 0.2
		i = i + 1
		
