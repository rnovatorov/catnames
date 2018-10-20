from contextlib import contextmanager

import trio

from . import filters
from .game import Game
from .utils import conjunct


class Dispatcher:

    def __init__(self, bot):
        self.bot = bot
        self.chat_ids = set()

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.new_game_handler, nursery)

    async def new_game_handler(self, nursery):
        async for event in self.bot.sub(conjunct(
            filters.new_msg,
            filters.chat_msg,
            self.filter_new_chat,
            filters.game_request
        )):
            await nursery.start(self.new_game, event)

    async def new_game(self, event, task_status=trio.TASK_STATUS_IGNORED):
        chat_id = event['object']['peer_id']
        with self.chat_scope(chat_id):
            task_status.started()
            game = await Game.new(self.bot, chat_id)
            await game.start()

    @contextmanager
    def chat_scope(self, chat_id):
        self.chat_ids.add(chat_id)
        yield
        self.chat_ids.remove(chat_id)

    def filter_new_chat(self, e):
        chat_id = e['object']['peer_id']
        return chat_id not in self.chat_ids
