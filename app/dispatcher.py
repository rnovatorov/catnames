from contextlib import contextmanager

import trio

from .game import Game
from .filters import conv_msg, new_game_cmd


class Dispatcher:

    def __init__(self, bot):
        self.bot = bot
        self.conv_ids = set()

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            async for event in self.bot.sub(self.new_game_request):
                await nursery.start(self.start_game, event)

    async def start_game(self, event, task_status=trio.TASK_STATUS_IGNORED):
        conv_id = event['object']['peer_id']
        with self.conv_scope(conv_id):
            task_status.started()
            game = await Game.new(conv_id)
            await game.start()

    @contextmanager
    def conv_scope(self, conv_id):
        self.conv_ids.add(conv_id)
        yield
        self.conv_ids.remove(conv_id)

    def new_game_request(self, e):
        return conv_msg(e) and self.new_conv(e) and new_game_cmd(e)

    def new_conv(self, e):
        conv_id = e['object']['peer_id']
        return conv_id not in self.conv_ids
