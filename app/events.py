from . import bot


@bot.on('message_new')
async def echo(msg):
    await bot.vk.messages.send(
        peer_id=msg['peer_id'],
        message=msg['text'],
    )
