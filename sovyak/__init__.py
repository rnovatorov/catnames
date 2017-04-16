import logging
from flask import Flask
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from flask_login import LoginManager
from config import *


# Instantiating Flask
app = Flask(__name__)
app.config.from_object("config")

# Logging
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    fh = RotatingFileHandler("tmp/sovyak.log", "a", 1 * 1024 * 1024, 10)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    app.logger.setLevel(logging.INFO)
    fh.setLevel(logging.INFO)
    app.logger.addHandler(fh)
    app.logger.info("Sovyak startup")

# WebSockets
socketio = SocketIO(app)

# DB setup
mongo = PyMongo(app)

# Login manager conf
lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
lm.login_message_category = "info"

# For VK
from . import VKOAuther
vk_oauther = VKOAuther.VKOAuther(VK_APP_ID, VK_APP_SECRET,
                                 VK_REDIRECT_URI=VK_REDIRECT_URI)

# Importing views, models
from . import views, events, models
