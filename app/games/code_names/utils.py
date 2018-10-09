import os


HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = os.path.join(HERE, 'words')


def load_words(dict_name):
    with open(os.path.join(WORDS, dict_name), encoding='utf-8') as f:
        return f.read().split()
