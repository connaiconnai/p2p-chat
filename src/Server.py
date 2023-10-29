import threading
import socket


BACK_LOG = 10
BUFFER_SIZE = 1024


# for receiveing
class Server(threading.Thread):
    def __init__(self, port):
        super(Server, self).__init__()

        self.host = ""
        self.port = int(port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))

    def close(self):
        self.sock.close()

    def run(self):
        print(" === sub thread === ")
        self.sock.listen(BACK_LOG)
        conn, _ = self.sock.accept()
        while True:
            msg = conn.recv(BUFFER_SIZE).decode("utf-8")
            if msg == "q":
                break
            print("\n recv >" + msg)

        self.close()
