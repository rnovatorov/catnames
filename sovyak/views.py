from flask import render_template, flash, redirect, url_for, request, g
from flask_socketio import emit, send
from flask_login import login_user, logout_user, current_user, login_required
from sovyak import app, socketio, mongo, lm, vk_oauther
from .models import User


@app.before_request
def before_request():
    g.user = current_user


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",
        title="Home"
    )


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
        flash("Authentication failed (code is None)")
        return redirect(url_for("login"))
    vk_access_info = vk_oauther.get_access_token(code)
    if "error_description" in vk_access_info:
        flash("Authentication failed (%s)" % vk_access_info["error_description"])
        return redirect(url_for("login"))
    elif vk_access_info is None:
        flash("Authentication failed (%s)" % "vk_access_info is None")
        return redirect(url_for("login"))
    elif not "user_id" in vk_access_info:
        flash("Authentication failed (%s)" % "No user_id in vk_access_info")
        return redirect(url_for("login"))

    # Logging in
    if User.exists(vk_access_info["user_id"]): # User exists
        result = User.update(vk_access_info)
    else:                                      # New user
        result = User.register(vk_access_info)

    if not result["success"]:
        flash("Authentication failed (%s)" % result["reason"])
        return redirect(url_for("login"))

    u = User(vk_access_info["user_id"])
    u.set_online()
    login_user(u)

    # Emitting change of connected users
    socketio.emit("connected_users", 
                   u.json(),
                   namespace="/lobby")

    return redirect(url_for("lobby"))


@app.route("/login")
def login():
    return render_template("login.html",
        title="Login"
    )


@app.route("/logout")
@login_required
def logout():
    current_user.set_offline()
    # Emitting change of connected users
    socketio.emit("connected_users",
                   current_user.json(),
                   namespace="/lobby")
    logout_user()

    return redirect(url_for("index"))


@socketio.on("connect", namespace="/lobby")
def connect():
    # if current_user.is_authenticated():
    app.logger.info("User %s is online" % current_user.user_id)
    current_user.set_online()
    socketio.emit("connected_users", current_user.json(), namespace="/lobby")


@socketio.on("disconnect", namespace="/lobby")
def disconnect():
    # if current_user.is_authenticated():
    app.logger.info("User %s is offline" % current_user.user_id)
    current_user.set_offline()
    socketio.emit("connected_users", current_user.json(), namespace="/lobby")


@app.route("/lobby")
@login_required
def lobby():
    return render_template("lobby.html",
        title="Lobby",
        users_online=User.get_online_users()
    )

@app.route("/room/<int:room_number>")
@login_required
def room(room_number):
    return "Room number %d" % room_number


@app.route("/game")
@login_required
def game():
    return "The game"


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
    db.session.rollback()
    return render_template("500.html"), 500


def get_online_users_json():
    return [u.json() for u in User.get_online_users()]