import enum
import random
from dataclasses import dataclass

import more_itertools as mit

from . import config


class TileColor(enum.Enum):

    BLUE = 'blue'
    RED = 'red'
    WHITE = 'white'
    BLACK = 'black'

    def __repr__(self):
        return f'{self.name}'


@dataclass
class Tile:

    code_name : str
    color : TileColor
    flipped : bool = False

    def flip(self):
        self.flipped = not self.flipped


class Map:

    def __init__(self, tiles):
        self.tiles = tiles

    @classmethod
    def random(cls):
        code_names = random.sample(config.CODE_NAMES, config.N_TOTAL)
        tiles = [
            Tile(code_name=code_names.pop(), color=color)
            for color in TileColor
            for _ in range(getattr(config, f'N_{color.name}'))
        ]
        random.shuffle(tiles)
        tiles = mit.chunked(tiles, config.SIDE_LEN)
        return cls(tiles=list(tiles))
