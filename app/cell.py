from dataclasses import dataclass
from contextlib import contextmanager

from . import config


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

    def as_button(self):
        raise NotImplementedError

    def as_emoji(self):
        raise NotImplementedError
