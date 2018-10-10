from dataclasses import dataclass
from contextlib import contextmanager

from PIL import Image, ImageDraw

from app.games.code_names import config


@dataclass
class Cell:

    word: str
    color: tuple
    flipped: bool = False

    def flip(self):
        self.flipped = not self.flipped

    @contextmanager
    def color_up(self):
        old_flipped = self.flipped
        self.flipped = True
        yield
        self.flipped = old_flipped

    def as_img(self, font):
        color = self.color if self.flipped else config.COLOR_GREY

        img = Image.new('RGB', config.CELL_SIZE, color)
        draw = ImageDraw.Draw(img)

        draw.rectangle(
            (0, 0, config.CELL_WIDTH, config.CELL_HEIGHT),
            width=config.BORDER_WIDTH,
            outline=config.BORDER_COLOR
        )

        if not self.flipped:
            word_width, word_height = draw.textsize(self.word, font=font)
            text_x = (config.CELL_WIDTH - word_width) / 2
            text_y = (config.CELL_HEIGHT - word_height) / 2
            draw.text((text_x, text_y), self.word, font=font)

        return img
