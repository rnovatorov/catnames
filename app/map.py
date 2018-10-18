import random

import more_itertools as mit

from . import config
from .cell import BlueCell, RedCell, NeutralCell, KillerCell


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
        return '\n'.join(
            ' '.join(cell.as_emoji() for cell in row)
            for row in self.cells
        )

    def _build_dict(self):
        self._dict = {
            cell.word: (x, y)
            for y, row in enumerate(self.cells)
            for x, cell in enumerate(row)
        }

    @classmethod
    def random(cls, words):
        assert len(words) == len(set(words))
        assert len(words) >= config.N_TOTAL_CELLS

        words = random.sample(words, config.N_TOTAL_CELLS)

        cells = [
            BlueCell(word=words.pop())
            for _ in range(config.N_BLUE_CELLS)
        ] + [
            RedCell(word=words.pop())
            for _ in range(config.N_RED_CELLS)
        ] + [
            NeutralCell(word=words.pop())
            for _ in range(config.N_NEUTRAL_CELLS)
        ] + [
            KillerCell(word=words.pop())
            for _ in range(config.N_KILLER_CELLS)
        ]

        random.shuffle(cells)
        matrix = mit.chunked(cells, config.N_CELLS_IN_ROW)

        return cls(cells=list(matrix))
