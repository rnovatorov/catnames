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
    return redirect(vk_oauther.compose_auth_url())


@app.route("/vk_oauth_callback")
def vk_oauth_callback():
    code = request.args.get("code")
    if code is None:
        flash("Authentication failed (code is None)")
        return redirect(url_for("login"))
    vk_user_info = vk_oauther.get_access_token(code)
    if vk_user_info is None or "error_description" in vk_user_info:
        flash("Authentication failed (%s)" % vk_user_info["error_description"])
        return redirect(url_for("login"))

    # Logging in
    doc = {
        "_id": vk_user_info["user_id"],
        "access_token": vk_user_info["access_token"],
        "expires_in": vk_user_info["expires_in"],
        "online": True
    }
    u = User(doc["_id"])
    if mongo.db.users.find_one({"_id": doc["_id"]}): # If user exists
        u.set_online()
    else:                                            # If new user
        mongo.db.users.insert_one(doc)
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
    g.user.set_offline()
    # Emitting change of connected users
    socketio.emit("connected_users",
                   g.user.json(),
                   namespace="/lobby")
    logout_user()

    return redirect(url_for("index"))
 

@app.route("/lobby")
@login_required
def lobby():
    return render_template("lobby.html",
        title="Lobby",
        users_online=User.get_online_users()
    )


@app.route("/game")
@login_required
def game():
    pass


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
    return [{"user_id": u.user_id,
             "full_name": u.full_name,
             "avatar": u.avatar}
             for u in User.get_online_users()]