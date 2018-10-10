from app import utils


DICT_NAME = 'ru-nouns.txt'


def test_resource():
    words = utils.resource.word_list(DICT_NAME)
    assert 'наука' in words
