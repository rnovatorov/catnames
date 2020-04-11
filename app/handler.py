import contextlib

import trio
import attr

from .game import Game


@attr.s
class Handler:

    bot = attr.ib()
    chats = attr.ib(factory=set)

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

    @contextlib.contextmanager
    def chat_scope(self, chat_id):
        self.chats.add(chat_id)
        yield
        self.chats.remove(chat_id)

    def new_chat_message(self, update):
        msg = update.get("message")
        if msg is None:
            return False

        from_ = msg.get("from")
        if from_ is None:
            return False

        from_id = from_["id"]
        chat_id = msg["chat"]["id"]
        return from_id != chat_id and chat_id not in self.chats
