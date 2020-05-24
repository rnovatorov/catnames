import pathlib


WORDLISTS = pathlib.Path(__file__).parent.parent / "wordlists"


def load(name):
    with open(WORDLISTS / name, encoding="utf-8") as f:
        return f.read().split()


def list():
    return [path.parts[-1] for path in WORDLISTS.glob("*")]
