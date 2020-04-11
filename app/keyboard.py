import json
from dataclasses import dataclass


@dataclass
class Button:

    label: str
    color: str
    type: str = "text"

    def json(self):
        return {"action": {"type": self.type, "label": self.label}, "color": self.color}


@dataclass
class Keyboard:

    buttons: [[Button]]
    one_time: bool = False

    def json(self):
        return {
            "one_time": self.one_time,
            "buttons": [[button.json() for button in row] for row in self.buttons],
        }

    def dump(self, ensure_ascii=False):
        return json.dumps(self.json(), ensure_ascii=ensure_ascii)

    @classmethod
    def empty(cls):
        return cls(buttons=[], one_time=True)
