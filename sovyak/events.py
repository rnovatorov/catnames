from flask import session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from . import app, socketio


# Lobby
@socketio.on("connect", namespace="/lobby")
def connect():
    app.logger.info("User %s is in lobby" % current_user.user_id)
    current_user.set_in_lobby(True)
    socketio.emit("users_in_lobby", current_user.json(), namespace="/lobby")


@socketio.on("disconnect", namespace="/lobby")
def disconnect():
    app.logger.info("User %s is not in lobby" % current_user.user_id)
    current_user.set_in_lobby(False)
    socketio.emit("users_in_lobby", current_user.json(), namespace="/lobby")


# Game
@socketio.on("joined", namespace="/game")
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    join_room(room)
    app.logger.info("User %s is in game" % current_user.user_id)
    emit("status", {"msg": current_user.full_name + " has entered the room."}, room=room)


@socketio.on("text", namespace="/game")
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get("room")
    app.logger.info("User %s wrote: %s" % (current_user.user_id,
                                           message["msg"]))
    emit("message", {"msg": current_user.full_name + ":" + message["msg"]}, room=room)


@socketio.on("left", namespace="/game")
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    leave_room(room)
    app.logger.info("User %s has left the game" % current_user.user_id)
    emit("status", {"msg": current_user.full_name + " has left the room."}, room=room)
