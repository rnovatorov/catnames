import trio
from async_vk_bot import Bot

from .dispatcher import Dispatcher


async def main():
    bot = Bot()
    dispatcher = Dispatcher(bot)
    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(dispatcher)
