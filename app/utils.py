from contextlib import contextmanager

from . import config
from .resource import Resource
from .errors import BadFormat


resource = Resource()

uniset = type('anybody', (), {'__contains__': lambda self, _: True})()


@contextmanager
def ctx_if(cond, ctx_man):
    if cond:
        with ctx_man:
            yield
    else:
        yield


def conjunct(*ps):
    return lambda e: all(p(e) for p in ps)


def disjunct(*ps):
    return lambda e: any(p(e) for p in ps)


def empty_keyboard():
    return '{"buttons":[],"one_time":true}'


def strip_reference(text):
    match = config.RE_TEXT_WITH_REFERENCE.match(text)
    if match is None:
        raise BadFormat
    return match[1]


def get_word_and_number(text):
    match = config.RE_WORD_AND_NUMBER.match(text)
    if match is None:
        raise BadFormat
    word, number = match.groups()
    return word, int(number)


def match_wants_to_play(text):
    match = config.RE_WANTS_TO_PLAY.match(text)
    return match is not None


def match_stop_recruiting(text):
    match = config.RE_NO_MORE_PLAYERS.match(text)
    return match is not None
