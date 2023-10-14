# pyright: reportGeneralTypeIssues=false

from client import client 
from server import server

import threading

class parent:
    def __init__(self, port):
        self.server = server()
        listener = threading.Thread(target=self.server.run, daemon=True);
        listener.start()
        self.port = port

    def run(self):
        self.client = client(self.port)
        self.client.run()

if __name__ == '__main__':
    port = input('port: ')
    parent = parent(port)
    parent.run()
