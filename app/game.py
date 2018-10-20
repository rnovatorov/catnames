from . import config, filters, utils
from .map import Map
from .cells import BlueCell, RedCell, NeutralCell, KillerCell
from .errors import Unreachable


class BaseGame:

    def __init__(self, bot, chat_id, map_):
        self._bot = bot
        self._chat_id = chat_id
        self.map = map_

        self.finished = False
        self.blue_spymaster = None
        self.red_spymaster = None

    @property
    def spymasters(self):
        return self.blue_spymaster, self.red_spymaster

    async def _send(self, **kwargs):
        await self._bot.api.messages.send(**kwargs)

    async def _broadcast(self, **kwargs):
        await self._send(peer_id=self._chat_id, **kwargs)

    async def _sub_for_messages(self, *predicates):
        async for event in self._bot.sub(utils.conjunct(
            filters.new_msg,
            filters.chat_msg,
            filters.peer_ids([self._chat_id]),
            *predicates
        )):
            yield event['object']

    async def _wait_message(self, *predicates):
        event = await self._bot.wait(utils.conjunct(
            filters.new_msg,
            filters.chat_msg,
            filters.peer_ids([self._chat_id]),
            *predicates
        ))
        return event['object']

    @classmethod
    async def new(cls, bot, chat_id):
        words = utils.resource.words(config.WORD_LIST_NAME)
        map_ = Map.random(words=words)
        return cls(
            bot=bot,
            chat_id=chat_id,
            map_=map_
        )


class Game(BaseGame):

    async def start(self):
        await self.registration()
        await self.reveal_map_to_spymasters()
        await self.show_map()
        winner = await self.wait_winner()
        await self._broadcast(
            message=winner,
            keyboard=utils.empty_keyboard()
        )

    async def registration(self):
        for color, attr_name in [
            ('синим', 'blue_spymaster'),
            ('красным', 'red_spymaster')
        ]:
            await self._broadcast(message=f'Кто будет {color} спай-мастером?')
            msg = await self._wait_message()
            setattr(self, attr_name, msg['from_id'])

    async def reveal_map_to_spymasters(self):
        peer_ids = ','.join(str(spymaster) for spymaster in self.spymasters)
        await self._send(
            peer_ids=peer_ids,
            message=self.map.as_emojis()
        )

    async def show_map(self):
        await self._broadcast(
            message='Выбирайте слово.',
            keyboard=self.map.as_keyboard(one_time=False)
        )

    async def wait_winner(self):
        async for cell in self.wait_guesses():
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

    async def wait_guesses(self):
        async for msg in self._sub_for_messages():
            word = utils.strip_reference(msg['text'])

            try:
                cell = self.map[word]
            except KeyError:
                await self._broadcast(
                    message='Такого слова нет, тупица.'
                )
                continue

            if cell.flipped:
                await self._broadcast(
                    message='Слово уже перевернуто.'
                )
                continue

            yield cell
