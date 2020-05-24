import pytest

from catnames import wordlist, config


@pytest.mark.parametrize("name", wordlist.list())
def test_uniq(name):
    words = wordlist.load(name)
    assert len(words) > config.N_TOTAL_CELLS
    assert len(words) == len(set(words))
