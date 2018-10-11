from app import config
from app.map import Map
from app.utils import resource


def test_sanity():
    words = resource.words(config.WORD_LIST_NAME)
    map = Map.random(words)

    revealed_img = map.as_img(reveal=True)
    not_revealed_img = map.as_img(reveal=False)

    assert revealed_img != not_revealed_img
