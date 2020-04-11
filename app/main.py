import trio
import triogram

from .handler import Handler


async def app():
    bot = triogram.make_bot()
    handler = Handler(bot)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(handler)


def main():
    trio.run(app)
