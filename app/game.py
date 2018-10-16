from . import config
from .map import Map
from .team import Team
from .photo_uploader import PhotoUploader
from .filters import new_msg, chat_msg, peer_ids, from_ids
from .errors import Unreachable, ScrewedUp, BadFormat
from .utils import resource, conjunct, strip_reference, get_word_and_number


class BaseGame:

    def __init__(self, bot, chat_id, map):
        self._bot = bot
        self._chat_id = chat_id

        self._pu = PhotoUploader(api=self._bot.api)

        self.map = map
        self.blue_team = None
        self.red_team = None
        self.winner = None
        self.cur_team = None

    @property
    def teams(self):
        return self.blue_team, self.red_team

    async def _broadcast(self, msg):
        await self._send_msg(self._chat_id, msg)

    async def _send_msg(self, peer_id, msg):
        await self._bot.api.messages.send(
            peer_id=peer_id,
            message=msg
        )

    async def _wait_msg_from(self, ids):
        async for event in self._bot.sub(conjunct(
            new_msg, chat_msg,
            peer_ids([self._chat_id]),
            from_ids(ids)
        )):
            yield event['object']

    @classmethod
    async def new(cls, bot, chat_id):
        words = resource.words(config.WORD_LIST_NAME)
        map = Map.random(words=words)
        return cls(
            bot=bot,
            chat_id=chat_id,
            map=map
        )


class Game(BaseGame):

    async def start(self):
        await self.registration()

        await self.reveal_map_to_spymasters()
        while not self.winner:
            self.cur_team = self.another_team
            await self.play_round()

        await self.announce_winner()

    async def registration(self):
        # TODO
        raise NotImplementedError

    async def play_round(self):
        await self.show_map()
        await self.announce_cur_team()

        try:
            word, attempts = await self.get_word_and_number_from_spymaster()
        except ScrewedUp as exc:
            await self.blame_team(exc)
            return

        while not self.winner and attempts:
            try:
                cell = await self.get_team_guess()
            except ScrewedUp as exc:
                await self.blame_team(exc)
                return

            cell.flip()
            attempts -= 1

            if cell.color is self.cur_team.color:
                if self.map.all_flipped(self.cur_team.color):
                    self.winner = self.cur_team

            elif cell.color is self.another_team.color:
                if self.map.all_flipped(self.another_team.color):
                    self.winner = self.another_team

            elif cell.color is config.COLOR_WHITE:
                attempts = 0

            elif cell.color is config.COLOR_BLACK:
                self.winner = self.another_team

            else:
                raise Unreachable

    @property
    def another_team(self):
        if self.cur_team is self.blue_team:
            return self.red_team
        return self.blue_team

    async def reveal_map_to_spymasters(self):
        # TODO
        raise NotImplementedError

    async def show_map(self):
        # TODO
        raise NotImplementedError

    async def announce_winner(self):
        await self._broadcast(f'Победитель: {self.winner.name}!')

    async def announce_cur_team(self):
        await self._broadcast(f'Ход {self.cur_team.name}.')

    async def get_word_and_number_from_spymaster(self):
        async for msg in self._wait_msg_from([self.cur_team.spymaster_id]):
            text = strip_reference(msg['text'])

            try:
                word, number = get_word_and_number(text)
            except BadFormat:
                raise ScrewedUp('Неверный формат, придурок')

            if word in self.map:
                raise ScrewedUp('Ты еще карту им скинь, недоумок')

            if number not in range(config.MAX_GUESS_ATTEMPTS):
                raise ScrewedUp('Выбери число попроще, дубина')

            return word, number

    async def get_team_guess(self):
        async for msg in self._wait_msg_from([self.cur_team.player_ids]):
            word = strip_reference(msg['text'])

            try:
                cell = self.map[word]
            except KeyError:
                raise ScrewedUp('Такого слова нет, тупица')

            if cell.flipped:
                raise ScrewedUp('Карточка уже перевернута, идиот')

            return cell

    async def blame_team(self, exc):
        await self._broadcast(f'{self.cur_team.name} облажалась: {exc}.')
