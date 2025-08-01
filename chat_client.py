import socketio

sio = socketio.Client()

def main():
    host = input("Enter server IP (e.g., 192.168.1.x): ")
    port = 5000
    username = input("Enter your username: ")

    @sio.event
    def connect():
        print("Connected to server.")

    @sio.event
    def disconnect():
        print("Disconnected from server.")

    @sio.on("message")
    def on_message(data):
        if isinstance(data, dict) and 'user' in data and 'text' in data:
            print(f"{data['user']}: {data['text']}")
        else:
            print(data)

    sio.connect(f"http://{host}:{port}")

    print("You can start typing messages. Press Ctrl+C to exit.")
    try:
        while True:
            msg = input()
            if msg.strip() == "":
                continue
            sio.send({'user': username, 'text': msg})
    except KeyboardInterrupt:
        pass
    finally:
        sio.disconnect()

if __name__ == "__main__":
    main()