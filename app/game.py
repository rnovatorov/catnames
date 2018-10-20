from . import config, filters, utils
from .map import Map
from .user import User
from .team import Team
from .cells import NeutralCell, KillerCell
from .errors import Unreachable, ScrewedUp, BadFormat


class BaseGame:

    def __init__(self, bot, chat_id, map_, blue_team, red_team):
        self._bot = bot
        self._chat_id = chat_id

        self.map = map_
        self.blue_team = blue_team
        self.red_team = red_team

        self.winner = None
        self.cur_team = None

    @property
    def teams(self):
        return self.blue_team, self.red_team

    @property
    def spymasters(self):
        return [team.spymaster for team in self.teams]

    async def _send(self, **kwargs):
        await self._bot.api.messages.send(**kwargs)

    async def _broadcast(self, **kwargs):
        await self._send(peer_id=self._chat_id, **kwargs)

    async def _wait_msg(self, from_=utils.uniset, ignore=()):
        event = await self._bot.wait(utils.conjunct(
            filters.new_msg,
            filters.chat_msg,
            filters.peer_ids([self._chat_id]),
            filters.from_ids(from_),
            filters.not_from_ids(ignore)
        ))
        return event['object']

    @classmethod
    async def new(cls, bot, chat_id):
        words = utils.resource.words(config.WORD_LIST_NAME)
        map_ = Map.random(words=words)

        blue_team = Team.blue()
        red_team = Team.red()

        return cls(
            bot=bot,
            chat_id=chat_id,
            map_=map_,
            blue_team=blue_team,
            red_team=red_team
        )


class Game(BaseGame):

    async def start(self):
        await self.registration()

        await self.reveal_map_to_spymasters()
        while not self.winner:
            self.cur_team = self.another_team
            await self.play_round()

        await self.announce_winner()

    def in_any_team(self, player):
        return any(player in team for team in self.teams)

    async def registration(self):
        roman = User(47439750)
        sovyak = User(398463689)

        for team in self.teams:
            team.players.add(roman)
            team.players.add(sovyak)
            team.spymaster = roman

    async def play_round(self):
        await self.announce_cur_team()
        await self.show_map_to_teams()

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

            if isinstance(cell, self.cur_team.cell_class):
                if self.map.all_flipped(self.cur_team.cell_class):
                    self.winner = self.cur_team

            elif isinstance(cell, self.another_team.cell_class):
                if self.map.all_flipped(self.another_team.cell_class):
                    self.winner = self.another_team

            elif isinstance(cell, NeutralCell):
                attempts = 0

            elif isinstance(cell, KillerCell):
                self.winner = self.another_team

            else:
                raise Unreachable

    @property
    def another_team(self):
        if self.cur_team is self.blue_team:
            return self.red_team
        return self.blue_team

    async def reveal_map_to_spymasters(self):
        peer_ids = ','.join(
            str(spymaster.id)
            for spymaster in self.spymasters
        )
        await self._send(
            peer_ids=peer_ids,
            message=self.map.as_emojis()
        )

    async def show_map_to_teams(self):
        await self._broadcast(
            message='Накидывайте варики.',
            keyboard=self.map.as_keyboard(one_time=False)
        )

    async def announce_winner(self):
        await self._broadcast(
            message=f'Победитель: {self.winner.name}!'
        )

    async def announce_cur_team(self):
        await self._broadcast(
            message=f'Ход {self.cur_team.name}.'
        )

    async def get_word_and_number_from_spymaster(self):
        msg = await self._wait_msg(from_=[self.cur_team.spymaster.id])
        text = utils.strip_reference(msg['text'])

        try:
            word, number = utils.get_word_and_number(text)
        except BadFormat:
            raise ScrewedUp('Неверный формат, придурок')

        if word in self.map:
            raise ScrewedUp('Ты еще карту им скинь, недоумок')

        if number not in range(config.MAX_GUESS_ATTEMPTS):
            raise ScrewedUp('Выбери число попроще, дубина')

        return word, number

    async def get_team_guess(self):
        msg = await self._wait_msg(from_=[
            player.id
            for player in self.cur_team
        ], ignore=[
            self.cur_team.spymaster
        ])
        word = utils.strip_reference(msg['text'])

        try:
            cell = self.map[word]
        except KeyError:
            raise ScrewedUp('Такого слова нет, тупица')

        if cell.flipped:
            raise ScrewedUp('Карточка уже перевернута, идиот')

        return cell

    async def blame_team(self, exc):
        await self._broadcast(
            message=f'{self.cur_team.name} облажалась: {str(exc)}.'
        )
