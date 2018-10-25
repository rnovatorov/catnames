import re
import math
from pathlib import Path


# Misc
APP_NAME = 'vk-code-names'
APP_DIR = Path(__file__).parent

# Regexps
RE_GAME_REQUEST = re.compile(r'^go|го')
RE_TEXT_WITH_REFERENCE = re.compile(r'^\[.+\|.+\]\s?,?\s?(.*?)$')

# Button colors
BUTTON_COLOR_NEGATIVE = 'negative'
BUTTON_COLOR_POSITIVE = 'positive'
BUTTON_COLOR_DEFAULT = 'default'
BUTTON_COLOR_PRIMARY = 'primary'

# Emojis
EMOJI_BLUE_HEART = '💙'
EMOJI_GREEN_HEART = '💚'
EMOJI_RED_HEART = '❤'
EMOJI_BLACK_HEART = '🖤'

# Map
N_BLUE_CELLS = 8
N_RED_CELLS = 7
N_NEUTRAL_CELLS = 4
N_KILLER_CELLS = 1
N_TOTAL_CELLS = sum([
    N_BLUE_CELLS,
    N_RED_CELLS,
    N_NEUTRAL_CELLS,
    N_KILLER_CELLS
])
N_CELLS_IN_ROW = 4
N_CELLS_IN_COL = 5
assert N_CELLS_IN_ROW * N_CELLS_IN_COL == N_TOTAL_CELLS

# Game
MAX_WORD_LEN = 8
ALLOW_CHOOSING_WORD_LIST = False
DEFAULT_WORD_LIST_NAME = 'nouns-ru.txt'
