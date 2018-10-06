"""
# Pseudo code for the game:
async def code_names():
    teams = make_teams()
    b_team, r_team = teams

    b_team.spymaster = random.choice(b_team)
    r_team.spymaster = random.choice(r_team)

    map = create_random_map()

    winner = None
    cur_team = b_team

    def another_team():
        return r_team if cur_team is b_team else b_team

    for team in teams:
        await send(team.spymaster, map.as_img(reveal=True))

    while not winner:
        await broadcast(f'{cur_team}\'s turn')

        mistake = False

        await broadcast(map.as_img(reveal=False))

        word, n_cells = await msg_from(cur_team.spymaster)
        assert n_cells.is_integer() and n_cells > 0

        while not mistake and n_cells:
            word = await msg_from(cur_team)

            cell = map[word]
            cell.flip()

            if cell.color is not cur_team.color:
                mistake = True

                if cell.color is Color.BLACK:
                    winner = another_team()

        winner = winner or map.winner()

        if winner:
            await broadcast(f'winner is {cur_team}')

        else:
            cur_team = another_team()
"""


from .map import Map
from .utils import load_words


class CodeNames:

    def __init__(self, map):
        self.map = map

    @classmethod
    def create(cls, dict_name='ru-nouns.txt'):
        words = load_words(dict_name)
        map = Map.random(words)
        return cls(map)
