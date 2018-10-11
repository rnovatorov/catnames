import re
import math
from pathlib import Path


# Misc
APP_NAME = 'vk-code-names'
APP_DIR = Path(__file__).parent

# Bot
RE_CMD_START = re.compile(r'играть')
RE_MSG_TEXT = re.compile(r'^\[.+\|.+\]\s?,?\s?(.*?)$')

# Colors
COLOR_BLUE = (61, 128, 168)
COLOR_RED = (231, 100, 90)
COLOR_WHITE = (213, 204, 183)
COLOR_BLACK = (44, 45, 40)
COLOR_GREY = (132, 141, 149)

# Words
WORD_LIST_NAME = 'ru-nouns.txt'
MAX_WORD_LEN = 16

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

# Cell size
CELL_WIDTH = 180
CELL_HEIGHT = 90
CELL_SIZE = (CELL_WIDTH, CELL_HEIGHT)

# Map size
MAP_WIDTH = CELLS_IN_ROW * CELL_WIDTH
MAP_HEIGHT = CELLS_IN_COL * CELL_HEIGHT
MAP_SIZE = (MAP_WIDTH, MAP_HEIGHT)

# Border
BORDER_WIDTH = 1
BORDER_COLOR = 'white'

# Font
FONT = 'UbuntuMono-R.ttf'
FONT_SIZE = 20
