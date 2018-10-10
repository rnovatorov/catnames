from app.utils import resource


DICT_NAME = 'ru-nouns.txt'


def test_resource():
    words = resource.word_list(DICT_NAME)
    assert 'наука' in words
