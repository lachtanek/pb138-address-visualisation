from .sample_streets import SampleStreetsVisualiser
from .biggest_towns import BiggestTownsVisualiser
from .extreme_street_names import ExtremeStreetNamesVisualiser
from .longest_streets import LongestStreetsVisualiser
from .profane_streets import ProfaneStreetsVisualiser
from .square_count import SquareCountVisualiser
from .town_with_most_streets import TownWithMostStreetsVisualiser

DEFAULT_VISUALISERS = [
	(SampleStreetsVisualiser, 'sample_streets'),
	(BiggestTownsVisualiser, 'biggest_towns'),
	(ExtremeStreetNamesVisualiser, 'extreme_street_names'),
	(LongestStreetsVisualiser, 'longest_streets'),
	(ProfaneStreetsVisualiser, 'profane_streets'),
	(SquareCountVisualiser, 'square_count'),
	(TownWithMostStreetsVisualiser, 'town_with_most_streets')
]
