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

    code_name: str
    color: Color
    flipped: bool = False

    def flip(self):
        self.flipped = not self.flipped


class Map:

    def __init__(self, cells):
        self.cells = cells

    @classmethod
    def random(cls):
        code_names = random.sample(config.CODE_NAMES, config.N_TOTAL)
        cells = [
            Cell(code_name=code_names.pop(), color=color)
            for color in Color
            for _ in range(getattr(config, f'N_{color.name}'))
        ]
        random.shuffle(cells)
        cells = mit.chunked(cells, config.SIDE_LEN)
        return cls(cells=list(cells))
