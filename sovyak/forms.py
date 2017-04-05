from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length
from app.models import User


class CreateRoomForm(FlaskForm):

    room_name = StringField("room_name", validators=[DataRequired(),
                                                     Length(min=1, max=64)])
    # room_password = StringField("room_password")
