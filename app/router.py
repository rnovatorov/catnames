from contextlib import contextmanager

import trio

from . import filters, utils
from .game import Game


class Router:
    def __init__(self, bot):
        self.bot = bot
        self.chat_ids = set()

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            async with self.bot.sub(
                utils.conjunct(filters.new_msg, filters.chat_msg, self.filter_new_chat)
            ) as events:
                async for event in events:
                    chat_id = event["object"]["peer_id"]
                    await nursery.start(self.new_game, chat_id)

    async def new_game(self, chat_id, task_status=trio.TASK_STATUS_IGNORED):
        with self.chat_scope(chat_id):
            task_status.started()
            game = Game(self.bot, chat_id)
            await game.start()

    @contextmanager
    def chat_scope(self, chat_id):
        self.chat_ids.add(chat_id)
        yield
        self.chat_ids.remove(chat_id)

    def filter_new_chat(self, e):
        chat_id = e["object"]["peer_id"]
        return chat_id not in self.chat_ids
