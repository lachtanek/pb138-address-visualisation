from .sample_streets import SampleStreetsVisualiser
from .biggestTowns import BiggestTownsVisualiser
from .extremeStreetNames import ExtremeStreetNamesVisualiser
# from .javaVisualiser import JavaVisualiser
from .longestStreets import LongestStreetsVisualiser
from .squareCount import SquareCountVisualiser
from .townWithMostStreets import TownWithMostStreetsVisualiser

DefaultSet = [
	(SampleStreetsVisualiser, 'sample_streets'),
	(BiggestTownsVisualiser, 'biggest_towns'),
	(ExtremeStreetNamesVisualiser, 'extreme_street_names'),
	(LongestStreetsVisualiser, 'longest_streets'),
	(SquareCountVisualiser, 'square_count'),
	(TownWithMostStreetsVisualiser, 'town_with_most_streets')
]
