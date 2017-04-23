import flask_socketio as fsio
from flask import session
from flask_login import current_user
from . import app, socketio


# Lobby
@socketio.on("connect", namespace="/lobby")
def connect_lobby():
    app.logger.info("User %s is in lobby" % current_user.user_id)
    current_user.set_in_lobby(True)
    socketio.emit("users_in_lobby", current_user.json(), namespace="/lobby")


@socketio.on("disconnect", namespace="/lobby")
def disconnect_lobby():
    app.logger.info("User %s is not in lobby" % current_user.user_id)
    current_user.set_in_lobby(False)
    socketio.emit("users_in_lobby", current_user.json(), namespace="/lobby")


# Game
@socketio.on("joined", namespace="/game")
def joined_game(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    fsio.join_room(room)
    app.logger.info("User %s is in room %s" % (current_user.user_id, room))
    fsio.emit("status", {
        "msg": current_user.full_name + " has entered the room.",
        "action": "connected",
        "u": current_user.json()
    }, room=room)


@socketio.on("user_input", namespace="/game")
def text_game(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get("room")
    app.logger.info("User %s wrote: %s" % (current_user.user_id,
                                           message["msg"]))
    fsio.emit("message", {
        "msg": current_user.full_name + ": " + message["msg"]
    }, room=room)


# @socketio.on("left", namespace="/game")
# def left_game(message):
#     """Sent by clients when they leave a room.
#     A status message is broadcast to all people in the room."""
#     room = session.get("room")
#     fsio.leave_room(room)
#     app.logger.info("User %s has left the game" % current_user.user_id)
#     fsio.emit("status", {
#         "msg": current_user.full_name + " has left the room.",
#         "action": "disconnected",
#         "user_id": current_user.user_id
#     }, room=room)


@socketio.on("disconnect", namespace="/game")
def disconnect_game():
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    fsio.leave_room(room)
    app.logger.info("User %s has left the game" % current_user.user_id)
    fsio.emit("status", {
        "msg": current_user.full_name + " has left the room.",
        "action": "disconnected",
        "u": current_user.json()
    }, room=room)
