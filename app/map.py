import random

import more_itertools as mit

from . import config
from .cell import Cell
from .utils import resource, ctx_if


class Map:

    def __init__(self, cells):
        self.cells = cells
        self._dict = None

    def __getitem__(self, word):
        if self._dict is None:
            self._build_dict()

        x, y = self._dict[word]
        return self.cells[y][x]

    def all_flipped(self, color):
        # TODO
        raise NotImplementedError

    def as_keyboard(self):
        # TODO
        raise NotImplementedError

    def as_emojis(self):
        # TODO
        raise NotImplementedError

    def _build_dict(self):
        self._dict = {
            cell.word: (x, y)
            for y, row in enumerate(self.cells)
            for x, cell in enumerate(row)
        }

    @classmethod
    def random(cls, words):
        assert len(words) == len(set(words))
        assert len(words) >= config.TOTAL_CELLS

        words = random.sample(words, config.TOTAL_CELLS)

        cells = [
            Cell(word=words.pop(), color=config.COLOR_BLUE)
            for _ in range(config.BLUE_CELLS)
        ] + [
            Cell(word=words.pop(), color=config.COLOR_RED)
            for _ in range(config.RED_CELLS)
        ] + [
            Cell(word=words.pop(), color=config.COLOR_WHITE)
            for _ in range(config.WHITE_CELLS)
        ] + [
            Cell(word=words.pop(), color=config.COLOR_BLACK)
            for _ in range(config.BLACK_CELLS)
        ]

        random.shuffle(cells)
        matrix = mit.chunked(cells, config.CELLS_IN_ROW)

        return cls(cells=list(matrix))
