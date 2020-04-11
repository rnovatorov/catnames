from app import wordlist


def test_load():
    words = wordlist.load("nouns-ru.txt")
    assert "наука" in words
