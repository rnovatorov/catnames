from contextlib import contextmanager

from . import config
from .resource import Resource


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


def get_msg_text(msg):
    raw = msg['text']
    match = config.RE_MSG_TEXT.match(raw)
    if match is None:
        raise RuntimeError(f'Unexpected fmt: {raw!r}')
    return match[1]
