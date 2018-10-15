from . import config
from .utils import get_msg_text


def new_msg(e):
    return e['type'] == 'message_new'


def chat_msg(e):
    return e['object']['peer_id'] != e['object']['from_id']


def game_request(e):
    msg = e['object']
    text = get_msg_text(msg)
    match = config.RE_GAME_REQUEST.match(text)
    return match is not None
