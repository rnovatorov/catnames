from app.utils import resource


DICT_NAME = 'ru-nouns.txt'


def test_resource():
    words = resource.words(DICT_NAME)
    assert 'наука' in words
