from pathlib import Path


WORDLISTS = Path(__file__).parent.parent / "wordlists"


def load(name):
    with open(WORDLISTS / name, encoding="utf-8") as f:
        return f.read().split()
