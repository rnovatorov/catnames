from app.games.code_names import utils


DICT_NAME = 'ru-nouns.txt'


def test_sanity():
    words = utils.load_words(DICT_NAME)
    assert 'наука' in words
