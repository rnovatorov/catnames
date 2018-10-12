from contextlib import contextmanager

import trio

from . import config
from .game import Game
from .utils import get_msg_text


class Dispatcher:

    def __init__(self, bot):
        self.bot = bot
        self.conv_ids = set()

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            async for msg in self.get_conv_messages():
                text = get_msg_text(msg)
                conv_id = msg['peer_id']
                if self.match_start_game(text):
                    nursery.start_soon(self.start_game, conv_id)

    async def start_game(self, conv_id):
        if conv_id not in self.conv_ids:
            with self.conv_scope(conv_id):
                game = await Game.new(conv_id)
                await game.start()

    @contextmanager
    def conv_scope(self, conv_id):
        self.conv_ids.add(conv_id)
        yield
        self.conv_ids.remove(conv_id)

    async def get_conv_messages(self):
        async for event in self.bot.sub(lambda e: (
            e['type'] == 'message_new'
            and
            e['object']['peer_id'] != e['object']['from_id']
        )):
            yield event['object']

    @staticmethod
    def match_start_game(text):
        match = config.RE_CMD_START.match(text)
        return match is not None
