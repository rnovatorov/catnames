import flask_socketio as fsio
from flask import render_template, flash, redirect, url_for, request, g, session
from flask_login import login_user, logout_user, current_user, login_required
from sovyak import app, socketio, mongo, lm, vk_oauther
from .models import User, Room
from .forms import CreateRoomForm, EnterRoomForm


@app.before_request
def before_request():
    g.user = current_user


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/vk_oauth")
def vk_oauth():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    return redirect(vk_oauther.compose_auth_url())


@app.route("/vk_oauth_callback")
def vk_oauth_callback():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    code = request.args.get("code")
    if code is None:
        flash("Authentication failed (code is None).", "danger")
        return redirect(url_for("login"))
    vk_access_info = vk_oauther.get_access_token(code)
    if vk_access_info is None:
        flash("Authentication failed (%s)." % "vk_access_info is None", "danger")
        return redirect(url_for("login"))
    elif "error_description" in vk_access_info:
        flash("Authentication failed (%s)." % vk_access_info["error_description"], "danger")
        return redirect(url_for("login"))
    elif not "user_id" in vk_access_info:
        flash("Authentication failed (%s)." % "No user_id in vk_access_info", "danger")
        return redirect(url_for("login"))

    # Logging in
    if User.exists(vk_access_info["user_id"]): # User exists
        result = User.update(vk_access_info)
    else:                                      # New user
        result = User.register(vk_access_info)

    if not result["success"]:
        flash("Authentication failed (%s)." % result["reason"], "danger")
        return redirect(url_for("login"))

    u = User(vk_access_info["user_id"])
    login_user(u)

    return redirect(url_for("index"))


@app.route("/login")
def login():
    return render_template("login.html",
        title="Login"
    )


@app.route("/logout")
@login_required
def logout():
    room_name = current_user.in_room()
    if room_name is not None:
        r = Room(room_name)
        r.remove_member(current_user.user_id)
        current_user.set_in_room(None)
        current_user.set_role(None)
        flash("You left room '%s'." % room_name, "warning")

        if not r.members():
            # Emitting change of available rooms
            socketio.emit("available_rooms", r.json(), namespace="/lobby")
            r.delete_room()
            flash("Room '%s' has been deleted" % room_name, "warning")

    logout_user()

    flash("Goodbye!", "warning")
    return redirect(url_for("index"))


@app.route("/lobby", methods=["GET", "POST"])
@login_required
def lobby():
    # Disallowing lobby for users who already are in a room
    if current_user.in_room() is not None:
        flash("Lobby is not accessible while in room.", "warning")
        return redirect(url_for("room", room_name=current_user.in_room()))

    # Dealing with room creation
    form = CreateRoomForm(creator=current_user)
    if form.validate_on_submit():
        room_name = form.room_name.data
        room_password = form.room_password.data
        role = form.role.data

        r = Room(room_name)
        r.set_password(room_password)
        r.add_member(current_user.user_id)
        current_user.set_in_room(room_name)
        current_user.set_role(role)
        session["room"] = room_name

        # Emitting change of available rooms
        socketio.emit("available_rooms", r.json(), namespace="/lobby")

        flash("Room '%s' has been created." % room_name, "warning")
        return redirect(url_for("room", room_name=room_name))

    return render_template("lobby.html",
        title="Lobby",
        form=form,
        available_rooms=Room.get_available_rooms(),
        users_in_lobby=User.get_users_in_lobby()
    )

@app.route("/room/<room_name>/enter/as/<role>", methods=["GET", "POST"])
@login_required
def enter_room(room_name, role):
    if not Room.room_name_exists(room_name):
        flash("Room '%s' does not exist." % room_name, "danger") 
        return redirect(url_for("lobby"))

    # Redirecting users who already are in this room
    if current_user.in_room() == room_name:
        return redirect(url_for("room", room_name=room_name))

    # Disallowing entering for users who already are in a room
    if current_user.in_room() is not None:
        flash("Lobby is not accessible while in room.", "danger")
        return redirect(url_for("room", room_name=current_user.in_room()))

    r = Room(room_name)

    # Room must have only one quiz-master
    if role == "quiz-master" and r.quiz_master():
        flash("Room already has a Quiz-Master.", "danger")
        return redirect(url_for("lobby"))

    # Checking room password and setting roles
    form = EnterRoomForm()
    if not r.password() or form.validate_on_submit():
        if r.password() and form.room_password.data != r.password():
            flash("Incorrect password", "danger")
            return redirect(url_for("enter_room", room_name=room_name,
                                    role=role))
        current_user.set_in_room(room_name)
        current_user.set_role(role)
        r.add_member(current_user.user_id)
        session["room"] = room_name

        # Emitting change of available rooms
        socketio.emit("available_rooms", r.json(), namespace="/lobby")
        # And new user in room
        socketio.emit("users_in_room", r.json(),
                       namespace="/room_%s" % room_name)

        flash("Entered as '%s'." % role, "warning")
        return redirect(url_for("room", room_name=room_name))

    return render_template("enter_room.html",
        title="Enter room",
        form=form,
        room_name=room_name,
        role=role
    )


@app.route("/room/<room_name>")
@login_required
def room(room_name):
    if not Room.room_name_exists(room_name):
        flash("Room '%s' does not exist." % room_name, "danger") 
        return redirect(url_for("lobby"))
    elif current_user.in_room() != room_name:
        flash("You are in another room")
        return redirect(url_for("room", room_name=current_user.in_room()))

    r = Room(room_name)

    return render_template("room.html",
        room_name=room_name,
        members=r.members()
    )


@app.route("/room/leave/<room_name>")
@login_required
def leave_room(room_name):
    if current_user.in_room() != room_name:
        flash("You can not leave room you are not in.", "danger")
        return redirect(url_for("lobby"))
    elif not Room.room_name_exists(room_name):
        flash("Room '%s' does not exist." % room_name, "danger") 
        return redirect(url_for("lobby"))

    # room = session.get("room")
    # app.logger.info("Session: %s" % session)
    # fsio.leave_room(room, sid=session["_id"], namespace="/game")
    # app.logger.info("User %s has left the game" % current_user.user_id)
    # socketio.emit("status",
    #              {"msg": current_user.full_name + " has left the room."},
    #              room=room,
    #              namespace="/game")

    r = Room(room_name)
    r.remove_member(current_user.user_id)
    current_user.set_in_room(None)
    current_user.set_role(None)

    flash("You left room '%s'." % room_name, "warning")

    if not r.members():
        # Emitting change of available rooms
        socketio.emit("available_rooms", r.json(), namespace="/lobby")
        r.delete_room()
        flash("Room '%s' has been deleted" % room_name, "warning")

    return redirect(url_for("lobby"))


@lm.user_loader
def load_user(user_id):  
    u = mongo.db.users.find_one({"_id": user_id})
    if not u:
        return None
    return User(u["_id"])


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500
