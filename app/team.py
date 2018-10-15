from . import config


class Team:

    def __init__(self, name, color, spymaster_id, player_ids):
        self.name = name
        self.color = color
        self.spymaster_id = spymaster_id
        self.player_ids = player_ids

    @property
    def member_ids(self):
        return self.player_ids + [self.spymaster_id]

    @classmethod
    def blue(cls, spymaster_id, player_ids):
        return cls(
            name='Team Blue',
            color=config.COLOR_BLUE,
            spymaster_id=spymaster_id,
            player_ids=player_ids
        )

    @classmethod
    def red(cls, spymaster_id, player_ids):
        return cls(
            name='Team Red',
            color=config.COLOR_RED,
            spymaster_id=spymaster_id,
            player_ids=player_ids
        )
