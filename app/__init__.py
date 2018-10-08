import trio
from async_vk_bot import Bot


async def main():
    bot = Bot()
    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
