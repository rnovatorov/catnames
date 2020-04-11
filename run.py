import trio
import triogram

from app.handler import Handler


async def main():
    bot = triogram.make_bot()
    handler = Handler(bot)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(handler)


if __name__ == "__main__":
    trio.run(main)
