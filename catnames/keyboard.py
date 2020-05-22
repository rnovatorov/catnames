import attr


@attr.s(auto_attribs=True)
class Keyboard:

    buttons: [[str]]
    one_time: bool = False
    resize: bool = True

    def json(self):
        return {
            "one_time_keyboard": self.one_time,
            "resize_keyboard": self.resize,
            "keyboard": self.buttons,
        }
