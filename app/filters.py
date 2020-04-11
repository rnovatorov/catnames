from . import config
from .utils import strip_reference


def new_msg(e):
    return e["type"] == "message_new"


def chat_msg(e):
    return e["object"]["peer_id"] != e["object"]["from_id"]


def peer_ids(ids):
    def predicate(e):
        return e["object"]["peer_id"] in ids

    return predicate
