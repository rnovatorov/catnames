from app import wordlist, config


def test_load_default():
    words = wordlist.load(config.DEFAULT_WORDLIST_NAME)
    assert len(words) > config.N_TOTAL_CELLS
    assert len(words) == len(set(words))
