import os

import trio
import async_vk_api
import async_vk_bot

from app.router import Router


async def main():
    api = async_vk_api.make_api(
        access_token=os.getenv("VK_API_ACCESS_TOKEN"), version="5.89"
    )
    bot = async_vk_bot.make_bot(api)
    router = Router(bot)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(bot)
        nursery.start_soon(router)


if __name__ == "__main__":
    trio.run(main)
