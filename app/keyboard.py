import attr


@attr.s(auto_attribs=True)
class Button:

    label: str
    color: str

    def json(self):
        # FIXME: Use emojis for coloring.
        return f"{self.color}: {self.label}"


@attr.s(auto_attribs=True)
class Keyboard:

    buttons: [[Button]]
    one_time: bool = False
    resize: bool = True

    def json(self):
        return {
            "one_time_keyboard": self.one_time,
            "resize_keyboard": self.resize,
            "keyboard": [[button.json() for button in row] for row in self.buttons],
        }
