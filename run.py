import trio
import triogram

from app.router import Router


async def main():
    bot = triogram.make_bot()
    router = Router(bot)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(router)


if __name__ == "__main__":
    trio.run(main)
