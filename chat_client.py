import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                break
            print(msg.decode())
        except:
            break

def main():
    host = input("Enter server IP (e.g., 192.168.1.x): ")
    port = 5000
    username = input("Enter your username: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    print("You can start typing messages. Press Ctrl+C to exit.")
    while True:
        try:
            msg = input()
            if msg.strip() == "":
                continue
            sock.send(f"{username}: {msg}".encode())
        except KeyboardInterrupt:
            break

    sock.close()

if __name__ == "__main__":
    main()
