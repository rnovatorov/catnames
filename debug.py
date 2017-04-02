#! venv/bin/python

from sovyak import app, socketio

socketio.run(app, debug=True)
