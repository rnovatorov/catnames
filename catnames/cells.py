import attr

from . import config


@attr.s(auto_attribs=True)
class Cell:

    word: str
    flipped: bool = False

    @property
    def emoji(self):
        raise NotImplementedError

    def flip(self):
        self.flipped = not self.flipped

    @property
    def label(self):
        return self.emoji if self.flipped else self.word


class BlueCell(Cell):
    @property
    def emoji(self):
        return config.EMOJI_BLUE_HEART


class RedCell(Cell):
    @property
    def emoji(self):
        return config.EMOJI_RED_HEART


class NeutralCell(Cell):
    @property
    def emoji(self):
        return config.EMOJI_GREEN_HEART


class KillerCell(Cell):
    @property
    def emoji(self):
        return config.EMOJI_BLACK_HEART
