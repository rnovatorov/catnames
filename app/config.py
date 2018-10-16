import re
import math
from pathlib import Path


# Misc
APP_NAME = 'vk-code-names'
APP_DIR = Path(__file__).parent

# Re
RE_GAME_REQUEST = re.compile(r'^погнали$')
RE_TEXT_WITH_REFERENCE = re.compile(r'^\[.+\|.+\]\s?,?\s?(.*?)$')
RE_WORD_AND_NUMBER = re.compile(r'^(\w+)\s(\d+)$')

# Colors
COLOR_BLUE = (61, 128, 168)
COLOR_RED = (231, 100, 90)
COLOR_WHITE = (213, 204, 183)
COLOR_BLACK = (44, 45, 40)
COLOR_GREY = (132, 141, 149)

# Number of cells
BLUE_CELLS = 9
RED_CELLS = 8
WHITE_CELLS = 7
BLACK_CELLS = 1
TOTAL_CELLS = sum([BLUE_CELLS, RED_CELLS, WHITE_CELLS, BLACK_CELLS])
CELLS_IN_ROW = math.sqrt(TOTAL_CELLS)
assert CELLS_IN_ROW.is_integer()
CELLS_IN_ROW = int(CELLS_IN_ROW)
CELLS_IN_COL = CELLS_IN_ROW

# Game
MAX_WORD_LEN = 16
MAX_GUESS_ATTEMPTS = max(BLUE_CELLS, RED_CELLS)
WORD_LIST_NAME = 'ru-nouns.txt'
