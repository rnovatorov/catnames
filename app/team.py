from .cells import BlueCell, RedCell


class Team:

    def __init__(self, name, cell_class):
        self.name = name
        self.cell_class = cell_class
        self.players = set()
        self.spymaster = None

    def __contains__(self, player):
        return player in self.players

    @classmethod
    def blue(cls):
        return cls(
            name='Blue team',
            cell_class=BlueCell,
        )

    @classmethod
    def red(cls):
        return cls(
            name='Red team',
            cell_class=RedCell,
        )
