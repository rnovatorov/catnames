import trio
import triogram

from .handler import Handler
from .logging import configure_logging


async def app():
    bot = triogram.make_bot()
    configure_logging()
    handler = Handler(bot)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(handler)


def main():
    trio.run(app)
