from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def handle_message(msg, *args):  # Accept extra arguments to avoid TypeError
    # Expect msg to be a dict: {'user': ..., 'text': ...}
    if isinstance(msg, dict) and 'user' in msg and 'text' in msg:
        formatted = f"{msg['user']}: {msg['text']}"
        send(formatted, broadcast=True)
    else:
        send(msg, broadcast=True)

if __name__ == "__main__":
    print("Starting Flask-SocketIO chat server...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
