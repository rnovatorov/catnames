from .map import Map
from .utils import load_words


class CodeNames:

    def __init__(self, map):
        self.map = map

    @classmethod
    def create(cls, dict_name='ru-nouns.txt'):
        words = load_words(dict_name)
        map = Map.random(words)
        return cls(map)
