import random
from dataclasses import dataclass

import more_itertools as mit
from PIL import Image, ImageDraw

from . import config


@dataclass
class Cell:

    word: str
    color: tuple
    flipped: bool = False

    def flip(self):
        self.flipped = not self.flipped

    def as_img(self):
        color = self.color if self.flipped else config.COLOR_GREY

        img = Image.new('RGB', config.PX_CELL_SIZE, color)
        draw = ImageDraw.Draw(img)

        draw.rectangle(
            (0, 0, config.PX_CELL_SIDE, config.PX_CELL_SIDE),
            width=config.BORDER_WIDTH,
            outline=config.BORDER_COLOR
        )

        if not self.flipped:
            draw.text((0, 0), self.word)

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

    def as_img(self, reveal=False):
        map_img = Image.new('RGB', config.PX_MAP_SIZE)

        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if reveal:
                    cell.flip()

                cell_img = cell.as_img()
                box = (
                    y * config.PX_CELL_SIDE,
                    x * config.PX_CELL_SIDE,
                    (y + 1) * config.PX_CELL_SIDE,
                    (x + 1) * config.PX_CELL_SIDE,
                )
                map_img.paste(cell_img, box)

                if reveal:
                    cell.flip()

        return map_img

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
