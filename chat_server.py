import socket
import threading

# Helper function to get the local IP address of the machine
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class ChatServer:
    def __init__(self, port=5000):
        self.host = get_local_ip()  # Bind to local network IP
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Chat server started on {self.host}:{self.port}")

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    self.clients.remove(client)
                    client.close()

    def handle_client(self, client_socket, addr):
        print(f"New connection from {addr}")
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    print(f"Connection closed by {addr}")
                    self.clients.remove(client_socket)
                    client_socket.close()
                    break
                print(f"[{addr}] {message.decode()}")
                self.broadcast(message, client_socket)
            except ConnectionResetError:
                print(f"Connection reset by {addr}")
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def start(self):
        print("Waiting for clients to connect...")
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
