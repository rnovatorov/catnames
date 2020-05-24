import attr
import trio

from . import wordlist
from .map import Map
from .keyboard import Keyboard
from .cells import BlueCell, RedCell, NeutralCell, KillerCell


@attr.s
class Game:

    _bot = attr.ib()
    _chat_id = attr.ib()
    map_ = attr.ib(default=None)
    finished = attr.ib(default=False)
    spymasters = attr.ib(factory=set)

    async def __call__(self):
        await self.create_map()
        await self.choose_spymasters()
        await self.reveal_map_to_spymasters()
        await self.show_map()
        winner = await self.wait_winner()
        await self._broadcast(winner, reply_markup={"remove_keyboard": True})

    async def create_map(self):
        name = await self.choose_wordlist()
        words = wordlist.load(name)
        self.map_ = Map.random(words=words)

    async def choose_wordlist(self):
        names = set(wordlist.list())

        async with self._sub_for_messages() as updates:
            reply_markup = Keyboard([list(names)]).json()
            await self._broadcast("Выберите словарь.", reply_markup=reply_markup)

            async for update in updates:
                name = update["message"]["text"]
                if name in names:
                    return name

                await self._broadcast("Такого словаря нет.")

    async def choose_spymasters(self):
        for i in range(1, 3):
            await self._broadcast(f"Кто будет {i}-ым ведущим?")
            update = await self._wait_message()
            self.spymasters.add(update["message"]["from"]["id"])

    async def reveal_map_to_spymasters(self):
        text = self.map_.as_emojis()
        async with trio.open_nursery() as nursery:
            for spymaster in self.spymasters:
                nursery.start_soon(self._send, spymaster, text)

    async def show_map(self):
        text = "Выберите клетку."
        reply_markup = self.map_.as_keyboard().json()
        await self._broadcast(text, reply_markup=reply_markup)

    async def wait_winner(self):
        async with self._sub_for_messages() as updates:
            async for update in updates:
                # FIXME: Parse text.
                word = update["message"]["text"]

                try:
                    cell = self.map_[word]
                except KeyError:
                    await self._broadcast("Такой клетки нет.")
                    continue

                if cell.flipped:
                    await self._broadcast("Клетка уже перевернута.")
                    continue

                cell.flip()

                if isinstance(cell, NeutralCell):
                    pass
                elif isinstance(cell, KillerCell):
                    return cell.emoji
                elif isinstance(cell, (BlueCell, RedCell)):
                    if self.map_.all_flipped(type(cell)):
                        return cell.emoji
                else:
                    raise RuntimeError("Unreachable")

                await self.show_map()

    async def _broadcast(self, text, **kwargs):
        await self._send(self._chat_id, text, **kwargs)

    async def _send(self, chat_id, text, **kwargs):
        await self._bot.api.send_message(
            json={"chat_id": chat_id, "text": text, **kwargs}
        )

    def _sub_for_messages(self):
        return self._bot.sub(self._new_message)

    async def _wait_message(self):
        return await self._bot.wait(self._new_message)

    def _new_message(self, update):
        msg = update.get("message")
        if msg is None:
            return False

        from_ = msg.get("from")
        if from_ is None:
            return False

        from_id = from_["id"]
        chat_id = msg["chat"]["id"]
        return from_id != chat_id and chat_id == self._chat_id
