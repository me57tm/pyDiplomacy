from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def twitch_ui():
    return render_template("index.html")


@socketio.event
def connect():
    pass
