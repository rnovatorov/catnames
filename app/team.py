from .cells import BlueCell, RedCell


class Team:

    def __init__(self, name, button_class, spymaster_id, player_ids):
        self.name = name
        self.button_class = button_class
        self.spymaster_id = spymaster_id
        self.player_ids = player_ids

    @property
    def member_ids(self):
        return self.player_ids + [self.spymaster_id]

    @classmethod
    def blue(cls, spymaster_id, player_ids):
        return cls(
            name='Team Blue',
            button_class=BlueCell,
            spymaster_id=spymaster_id,
            player_ids=player_ids
        )

    @classmethod
    def red(cls, spymaster_id, player_ids):
        return cls(
            name='Team Red',
            button_class=RedCell,
            spymaster_id=spymaster_id,
            player_ids=player_ids
        )
