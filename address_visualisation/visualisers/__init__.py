"""Package which contains instances of Visualiser."""
from .profane_streets import ProfaneStreetsVisualiser
from .biggest_towns import BiggestTownsVisualiser
from .extreme_street_names import ExtremeStreetNamesVisualiser
from .longest_streets import LongestStreetsVisualiser
from .square_count import SquareCountVisualiser
from .town_with_most_streets import TownWithMostStreetsVisualiser

DEFAULT_VISUALISERS = [
				(ProfaneStreetsVisualiser, 'profane_streets'),
				(BiggestTownsVisualiser, 'biggest_towns'),
				(ExtremeStreetNamesVisualiser, 'extreme_street_names'),
				(LongestStreetsVisualiser, 'longest_streets'),
				(SquareCountVisualiser, 'square_count'),
				(TownWithMostStreetsVisualiser, 'town_with_most_streets')
				]
