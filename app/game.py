import trio

from . import config
from .map import Map
from .team import Team
from .utils import resource


class BaseGame:

    def __init__(self, conv_id, map):
        self.conv_id = conv_id
        self.map = map

        self.blue_team = None
        self.red_team = None

        self.winner = None
        self.cur_team = None

    async def _broadcast(self, msg):
        raise NotImplementedError

    async def _send(self, peer_id, msg):
        raise NotImplementedError

    async def _msg_from(self, peer_id):
        raise NotImplementedError

    @classmethod
    async def new(cls, conv_id):
        words = resource.words(config.WORD_LIST_NAME)
        map = Map.random(words=words)
        return cls(conv_id=conv_id, map=map)


class Game(BaseGame):

    async def start(self):
        await self.registration()

        await self.reveal_map_to_spymasters()
        while not self.winner:
            self.cur_team = self.another_team
            await self.play_round()

        await self.announce_winner()

    async def registration(self):
        raise NotImplementedError

    async def play_round(self):
        await self.show_map_to_teams()
        await self.announce_cur_team()

        word, attempts = await self.get_word_and_number_from_spymaster()

        while not self.winner and attempts:
            word = await self.get_word_from_cur_team()

            cell = self.map[word]
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
                raise RuntimeError('Unreachable')

    @property
    def another_team(self):
        if self.cur_team is self.blue_team:
            return self.red_team
        return self.blue_team

    @property
    def teams(self):
        return self.blue_team, self.red_team

    async def reveal_map_to_spymasters(self):
        raise NotImplementedError

    async def show_map_to_teams(self):
        raise NotImplementedError

    async def announce_winner(self):
        raise NotImplementedError

    async def announce_cur_team(self):
        raise NotImplementedError

    async def get_word_and_number_from_spymaster(self):
        raise NotImplementedError

    async def get_word_from_cur_team(self):
        raise NotImplementedError
