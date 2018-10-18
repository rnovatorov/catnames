from dataclasses import dataclass
from contextlib import contextmanager

from . import config
from .errors import NoCellColor, NoCellEmoji


@dataclass
class Cell:

    word: str
    emoji: str = None
    button_color: str = None
    flipped: bool = False

    def flip(self):
        self.flipped = not self.flipped

    @contextmanager
    def color_up(self):
        old_flipped = self.flipped
        self.flipped = True
        yield
        self.flipped = old_flipped

    def as_button(self):
        if self.button_color is None and self.flipped:
            raise NoCellColor

        return {
            'action': {
                'type': 'text',
                'label': self.word
            },
            'color': self.button_color if self.flipped else config.BUTTON_COLOR_DEFAULT
        }

    def as_emoji(self):
        if self.emoji is not None:
            return self.emoji
        raise NoCellEmoji


class BlueCell(Cell):

    def __init__(self, word):
        super().__init__(
            word=word,
            emoji=config.EMOJI_BLUE_HEART,
            button_color=config.BUTTON_COLOR_PRIMARY
        )


class RedCell(Cell):

    def __init__(self, word):
        super().__init__(
            word=word,
            emoji=config.EMOJI_RED_HEART,
            button_color=config.BUTTON_COLOR_NEGATIVE
        )


class NeutralCell(Cell):

    def __init__(self, word):
        super().__init__(
            word=word,
            emoji=config.EMOJI_GREEN_HEART,
            button_color=config.BUTTON_COLOR_POSITIVE
        )


class KillerCell(Cell):

    def __init__(self, word):
        super().__init__(
            word=word,
            emoji=config.EMOJI_BLACK_HEART,
            button_color=None
        )
