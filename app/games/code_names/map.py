import enum
import random
from dataclasses import dataclass

import more_itertools as mit

from . import config


class Color(enum.Enum):

    BLUE = 'blue'
    RED = 'red'
    WHITE = 'white'
    BLACK = 'black'


@dataclass
class Cell:

    word: str
    color: Color
    flipped: bool = False

    def flip(self):
        self.flipped = not self.flipped


class Map:

    def __init__(self, cells):
        self.cells = cells
        self._dict = None

    def __getitem__(self, word):
        if self._dict is None:
            self._build_dict()

        y, x = self._dict[word]
        return self.cells[y][x]

    def _build_dict(self):
        self._dict = {
            cell.word: (y, x)
            for y, row in enumerate(self.cells)
            for x, cell in enumerate(row)
        }

    @classmethod
    def random(cls, words):
        assert len(words) >= config.N_TOTAL

        words = random.sample(words, config.N_TOTAL)
        cells = [
            Cell(word=words.pop(), color=color)
            for color in Color
            for _ in range(getattr(config, f'N_{color.name}'))
        ]
        random.shuffle(cells)
        cells = mit.chunked(cells, config.SIDE_LEN)

        return cls(cells=list(cells))
