from . import config
from .utils import get_msg_text


def conv_msg(e):
    return (
        e['type'] == 'message_new'
        and
        e['object']['peer_id'] != e['object']['from_id']
    )


def new_game_cmd(e):
    msg = e['object']
    text = get_msg_text(msg)
    match = config.RE_CMD_START.match(text)
    return match is not None
