import contextlib

import attr
import trio
import triogram
import pytest

from catnames.game import Game
from catnames.config import DEFAULT_WORDLIST_NAME


@attr.s
class MockApi:

    _fanout = attr.ib()

    async def __call__(self, method_name, kwargs):
        send_chan, recv_chan = trio.open_memory_channel(0)
        async with send_chan, recv_chan:
            args = kwargs.pop("json")
            await self._fanout.pub((method_name, args, send_chan.send))
            return await recv_chan.receive()

    def __getattr__(self, method_name):
        async def method(**kwargs):
            return await self(method_name, kwargs)

        return method


@attr.s
class MockBot:

    api = attr.ib()
    fanout = attr.ib(factory=triogram.Fanout)

    @property
    def sub(self):
        return self.fanout.sub

    async def wait(self, *args, **kwargs):
        async with self.sub(*args, **kwargs) as updates:
            return await updates.receive()


@pytest.fixture
async def new_game():
    fanout = triogram.Fanout()
    api = MockApi(fanout=fanout)
    bot = MockBot(api=api)

    async with contextlib.AsyncExitStack() as stack:
        nursery = await stack.enter_async_context(trio.open_nursery())
        api_calls = await stack.enter_async_context(fanout.sub())

        def factory(**kwargs):
            game = Game(bot=bot, **kwargs)
            nursery.start_soon(game)
            return bot.fanout, api_calls

        try:
            yield factory
        finally:
            nursery.cancel_scope.cancel()


class TestGame:
    def init(self, new_game):
        self.chat_id = 42
        self.updates, self.api_calls = new_game(chat_id=self.chat_id)
        self.player_1 = 1
        self.player_2 = 2

    async def test_run(self, new_game, autojump_clock):
        self.init(new_game)
        await self.choose_dict()
        await self.first_spymaster()
        await self.second_spymaster()

    async def choose_dict(self):
        method, args, send_response = await self.api_calls.receive()
        assert method == "send_message"
        assert args["text"] == "Выберите словарь."
        await send_response({})

        await trio.sleep(1)
        await self.updates.pub(
            {
                "message": {
                    "text": DEFAULT_WORDLIST_NAME,
                    "from": {"id": self.player_1},
                    "chat": {"id": self.chat_id},
                }
            }
        )

    async def first_spymaster(self):
        method, args, send_response = await self.api_calls.receive()
        assert method == "send_message"
        assert args["text"] == "Кто будет 1-ым ведущим?"
        await send_response({})

        await trio.sleep(1)
        await self.updates.pub(
            {
                "message": {
                    "text": "me",
                    "from": {"id": self.player_1},
                    "chat": {"id": self.chat_id},
                }
            }
        )

    async def second_spymaster(self):
        method, args, send_response = await self.api_calls.receive()
        assert method == "send_message"
        assert args["text"] == "Кто будет 2-ым ведущим?"
        await send_response({})

        await trio.sleep(1)
        await self.updates.pub(
            {
                "message": {
                    "text": "me",
                    "from": {"id": self.player_2},
                    "chat": {"id": self.chat_id},
                }
            }
        )
