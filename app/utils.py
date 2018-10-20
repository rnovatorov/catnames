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
