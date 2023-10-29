import threading
import socket

BACK_LOG = 10
BUFFER_SIZE = 1024


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connection(self):
        host = ""
        port = input("connection port >")
        self.sock.connect((host, int(port)))

    def message(self):
        while True:
            msg = input("message >")
            self.sock.send(msg.encode("utf-8"))
            if msg == "q":
                break
