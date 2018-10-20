from . import config
from .utils import strip_reference


def new_msg(e):
    return e['type'] == 'message_new'


def chat_msg(e):
    return e['object']['peer_id'] != e['object']['from_id']


def peer_ids(ids):
    def predicate(e):
        return e['object']['peer_id'] in ids
    return predicate


def game_request(e):
    text = strip_reference(e['object']['text'])
    match = config.RE_GAME_REQUEST.match(text)
    return match is not None
