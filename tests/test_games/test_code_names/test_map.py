from app.games.code_names import config
from app.games.code_names.map import Map


WORDS = ['foobar'] * config.TOTAL_CELLS


def test_sanity():
    map = Map.random(WORDS)

    revealed_img = map.as_img(reveal=True)
    not_revealed_img = map.as_img(reveal=False)

    assert revealed_img != not_revealed_img
