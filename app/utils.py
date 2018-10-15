from contextlib import contextmanager

from . import config
from .resource import Resource
from .errors import BadFormat


resource = Resource()


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
