from math import sqrt

def segment_length(seg):
	length = 0
	for i in range(1, len(seg)):
		length += sqrt((seg[i - 1][0] - seg[i][0]) ** 2 + (seg[i - 1][1] - seg[i][1]) ** 2)

	return length

def multi_segment_length(segs):
	return sum(map(segment_length, segs))
