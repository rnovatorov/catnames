from . import config
from .resource import Resource
from .errors import UnexpectedFormat


resource = Resource()


def conjunct(*ps):
    return lambda e: all(p(e) for p in ps)


def disjunct(*ps):
    return lambda e: any(p(e) for p in ps)


def empty_keyboard():
    return '{"buttons":[],"one_time":true}'


def strip_reference(text):
    match = config.RE_TEXT_WITH_REFERENCE.match(text)
    if match is None:
        raise UnexpectedFormat
    return match[1]
