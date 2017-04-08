from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Regexp
from sovyak.models import Room


class CreateRoomForm(FlaskForm):

    room_name = StringField("room_name", validators=[DataRequired(),
                                                     Length(min=1, max=32),
                                                     Regexp(r"[a-zA-Z0-9]+")])
    room_password = PasswordField("room_password", validators=[Length(min=0, max=32)])
    role = SelectField("role", choices=[("quiz-master", "Quiz-Master"),
                                        ("player", "Player"),
                                        ("spectator", "Spectator")])

    def __init__(self, creator, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.creator = creator

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        elif Room.room_name_exists(self.room_name.data):
            self.room_name.errors.append("Room '%s' already exists"
                                          % self.room_name.data)
            return False
        elif self.creator.in_room() is not None:
            self.room_name.errors.append("You already are in a room")
            return False
        elif self.role.data not in Room.roles:
            self.role.errors.append("Invalid role")
            return False
        else:
            return True


class EnterRoomForm(FlaskForm):

    room_password = PasswordField("room_password")
