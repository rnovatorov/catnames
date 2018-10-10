from string import ascii_lowercase

from app.games.code_names import config
from app.games.code_names.map import Map


def test_sanity():
    words = [ascii_lowercase[:config.MAX_WORD_LEN]] * config.TOTAL_CELLS
    map = Map.random(words)

    revealed_img = map.as_img(reveal=True)
    not_revealed_img = map.as_img(reveal=False)

    assert revealed_img != not_revealed_img
