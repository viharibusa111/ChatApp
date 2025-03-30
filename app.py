from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")


# Database setup
def create_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (room TEXT, username TEXT, message TEXT)''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("join")
def handle_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    send(f"{username} has joined the room.", room=room)

@socketio.on("message")
def handle_message(data):
    room = data["room"]
    username = data["username"]
    message = data["message"]

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (room, username, message) VALUES (?, ?, ?)", (room, username, message))
    conn.commit()
    conn.close()

    send(f"{username}: {message}", room=room)

@socketio.on("leave")
def handle_leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send(f"{username} has left the room.", room=room)

if __name__ == "__main__":
    create_db()
    socketio.run(app, debug=True)
