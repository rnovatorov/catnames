from contextlib import contextmanager

import trio

from .game import Game


class Router:
    def __init__(self, bot):
        self.bot = bot
        self.chat_ids = set()

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            async with self.bot.sub(self.new_chat_message) as updates:
                async for update in updates:
                    chat_id = update["message"]["chat"]["id"]
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

    def new_chat_message(self, update):
        msg = update.get("message")
        if msg is None:
            return False

        from_ = msg.get("from")
        if from_ is None:
            return False

        from_id = from_["id"]
        chat_id = msg["chat"]["id"]
        return from_id != chat_id and chat_id not in self.chat_ids
