import enum
import random
from dataclasses import dataclass

import more_itertools as mit
from PIL import Image

from . import config


class Color(enum.Enum):

    BLUE = (44, 45, 40)
    RED = (61, 128, 168)
    WHITE = (231, 100, 90)
    BLACK = (213, 204, 183)


@dataclass
class Cell:

    word: str
    color: Color
    flipped: bool = False

    def flip(self):
        self.flipped = not self.flipped

    def as_img(self, color=False, side=config.PX_CELL_SIDE):
        img = Image.new('RGB', (side, side))
        img.putdata((self.color.value,) * side * side)
        return img


class Map:

    def __init__(self, cells):
        self.cells = cells
        self._dict = None

    def __getitem__(self, word):
        if self._dict is None:
            self._build_dict()

        y, x = self._dict[word]
        return self.cells[y][x]

    def as_img(self, colors: bool):
        raise NotImplementedError

    def _build_dict(self):
        self._dict = {
            cell.word: (y, x)
            for y, row in enumerate(self.cells)
            for x, cell in enumerate(row)
        }

    @classmethod
    def random(cls, words):
        assert len(words) >= config.TOTAL_CELLS

        words = random.sample(words, config.TOTAL_CELLS)
        cells = [
            Cell(word=words.pop(), color=color)
            for color in Color
            for _ in range(config.count_cells(color))
        ]
        random.shuffle(cells)
        cells = mit.chunked(cells, config.CELLS_IN_ROW)

        return cls(cells=list(cells))
