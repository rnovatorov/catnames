import json


class Button:

    def __init__(self, label, color, type='text'):
        self.label = label
        self.color = color
        self.type = type

    def json(self):
        return {
            'action': {
                'type': self.type,
                'label': self.label
            },
            'color': self.color
        }


class Keyboard:

    def __init__(self, buttons, one_time=False):
        self.buttons = buttons
        self.one_time = one_time

    def json(self):
        return {
            'one_time': self.one_time,
            'buttons': [
                [button.json() for button in row]
                for row in self.buttons
            ]
        }

    def dump(self, ensure_ascii=False):
        return json.dumps(self.json(), ensure_ascii=ensure_ascii)

    @classmethod
    def empty(cls):
        return cls(buttons=[], one_time=True)
