from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Change this to a secure value

# Initialize SocketIO with eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)  # Broadcast the message to all clients

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)  # Ensure WebSockets work on Render
