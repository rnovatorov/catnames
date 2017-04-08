#! venv/bin/python

from sovyak import app, socketio

socketio.run(app, host="0.0.0.0")
