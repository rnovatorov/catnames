DICT_NAME = "nouns-ru.txt"


def test_resource(resource):
    words = resource.words(DICT_NAME)
    assert "наука" in words
