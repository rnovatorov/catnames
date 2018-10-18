from app import config
from app.map import Map
from app.utils import resource


def test_sanity():
    words = resource.words(config.WORD_LIST_NAME)
    map_ = Map.random(words=words)
    assert {
        config.EMOJI_BLUE_HEART,
        config.EMOJI_RED_HEART,
        config.EMOJI_GREEN_HEART,
        config.EMOJI_BLACK_HEART
    } == {
        cell.emoji
        for row in map_.cells
        for cell in row
    }
