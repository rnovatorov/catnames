from app.games.code_names import config
from app.games.code_names.map import Map


WORDS = ['foobar'] * config.TOTAL_CELLS


def test_sanity():
    map = Map.random(WORDS)
    img = map.cells[0][0].as_img()
