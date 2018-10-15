class Team:

    def __init__(self, name, color, spymaster, players):
        self.name = name
        self.color = color
        self.spymaster_id = spymaster
        self.player_ids = players

    @property
    def member_ids(self):
        return self.player_ids + [self.spymaster_id]
