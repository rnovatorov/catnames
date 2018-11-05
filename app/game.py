from async_vk_bot.utils import aclosed

from . import config, filters, utils
from .map import Map
from .cells import BlueCell, RedCell, NeutralCell, KillerCell
from .errors import Unreachable
from .keyboard import Keyboard


class BaseGame:

    def __init__(self, bot, chat_id):
        self._bot = bot
        self._chat_id = chat_id

        self.map = None
        self.finished = False
        self.spymasters = set()

    async def _send(self, **kwargs):
        await self._bot.api.messages.send(**kwargs)

    async def _broadcast(self, **kwargs):
        await self._send(peer_id=self._chat_id, **kwargs)

    @aclosed
    async def _sub_for_messages(self, *predicates):
        async with self._bot.sub(utils.conjunct(
            filters.new_msg,
            filters.chat_msg,
            filters.peer_ids([self._chat_id]),
            *predicates
        )) as events:
            async for event in events:
                yield event['object']

    async def _wait_message(self, *predicates):
        async with self._sub_for_messages(*predicates) as messages:
            async for msg in messages:
                return msg


class Game(BaseGame):

    async def start(self):
        await self.registration()
        await self.reveal_map_to_spymasters()
        await self.show_map()
        winner = await self.wait_winner()
        await self._broadcast(
            message=winner,
            keyboard=Keyboard.empty().dump()
        )

    async def registration(self):
        words = await self.wait_words()
        self.map = Map.random(words=words)

        for i in range(1, 3):
            await self._broadcast(message=f'Кто будет {i}-ым ведущим?')
            msg = await self._wait_message()
            self.spymasters.add(msg['from_id'])

    async def wait_words(self):
        # TODO: Implement.
        if config.ALLOW_CHOOSING_WORD_LIST:
            raise NotImplementedError

        else:
            word_list_name = config.DEFAULT_WORD_LIST_NAME

        return utils.resource.words(word_list_name)

    async def reveal_map_to_spymasters(self):
        peer_ids = ','.join(str(spymaster) for spymaster in self.spymasters)
        await self._send(
            peer_ids=peer_ids,
            message=self.map.as_emojis()
        )

    async def show_map(self):
        await self._broadcast(
            message='Выбирайте клетку.',
            keyboard=self.map.as_keyboard(one_time=False).dump()
        )

    async def wait_winner(self):
        async with self.wait_guesses() as guesses:
            async for cell in guesses:
                cell.flip()

                if isinstance(cell, NeutralCell):
                    pass

                elif isinstance(cell, KillerCell):
                    return cell.emoji

                elif isinstance(cell, (BlueCell, RedCell)):
                    if self.map.all_flipped(type(cell)):
                        return cell.emoji

                else:
                    raise Unreachable

                await self.show_map()

    @aclosed
    async def wait_guesses(self):
        async with self._sub_for_messages() as messages:
            async for msg in messages:
                word = utils.strip_reference(msg['text'])

                try:
                    cell = self.map[word]
                except KeyError:
                    await self._broadcast(
                        message='Такой клетки нет.'
                    )
                    continue

                if cell.flipped:
                    await self._broadcast(
                        message='Клетка уже перевернута.'
                    )
                    continue

                yield cell
