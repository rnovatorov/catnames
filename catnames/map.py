import random

import attr
import more_itertools as mit

from . import config
from .cells import BlueCell, RedCell, NeutralCell, KillerCell
from .keyboard import Keyboard


@attr.s
class Map:

    cells = attr.ib()
    _dict = attr.ib(default=None)

    def __contains__(self, word):
        return word in self._dict

    def __getitem__(self, word):
        if self._dict is None:
            self._build_dict()

        x, y = self._dict[word]
        return self.cells[y][x]

    def all_flipped(self, cell_class):
        return all(
            cell.flipped
            for row in self.cells
            for cell in row
            if isinstance(cell, cell_class)
        )

    def as_keyboard(self, **kwargs):
        return Keyboard(
            buttons=[[cell.label for cell in row] for row in self.cells], **kwargs
        )

    def as_emojis(self):
        return "\n".join(" ".join(cell.emoji for cell in row) for row in self.cells)

    def _build_dict(self):
        self._dict = {
            cell.word: (x, y)
            for y, row in enumerate(self.cells)
            for x, cell in enumerate(row)
        }

    @classmethod
    def random(cls, words):
        words = set(word for word in words if len(word) <= config.MAX_WORD_LEN)
        assert len(words) >= config.N_TOTAL_CELLS
        words = random.sample(words, config.N_TOTAL_CELLS)

        cells = (
            [BlueCell(words.pop()) for _ in range(config.N_BLUE_CELLS)]
            + [RedCell(words.pop()) for _ in range(config.N_RED_CELLS)]
            + [NeutralCell(words.pop()) for _ in range(config.N_NEUTRAL_CELLS)]
            + [KillerCell(words.pop()) for _ in range(config.N_KILLER_CELLS)]
        )
        random.shuffle(cells)
        cells = list(mit.chunked(cells, config.N_CELLS_IN_ROW))
        assert len(cells) == config.N_CELLS_IN_COL
        return cls(cells)
