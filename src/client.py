import threading
import socket

class BaseClient:
    def __init__(self, timeout:int=10, buffer:int=1024):
        self.__socket = None
        self.__address = None
        self.__timeout = timeout
        self.__buffer = buffer

    def connect(self, address, family:int, typ:int, proto:int):
        self.__address = address
        self.__socket = socket.socket(family, typ, proto)
        self.__socket.settimeout(self.__timeout)
        self.__socket.connect(self.__address)

    def send(self, message:str="") -> None:
        message_send = message
        self.__socket.send(message_send.encode('utf-8'))
        message_recv = self.__socket.recv(self.__buffer).decode('utf-8')
        self.received(message_recv)

    def received(self, message:str):
        print(message)


class InetClient(BaseClient):
    def __init__(self, host:str="0.0.0.0", port:int=8080) -> None:
        self.server=(host,port)
        super().__init__(timeout=60, buffer=1024)
        super().connect(self.server, socket.AF_INET, socket.SOCK_STREAM, 0)

class Client(threading.Thread):
    def __init__(self):
        super(Client, self).__init__()
        self.client = InetClient()
    def run(self):
        while True:
            msg = input("msg > ")
            self.client.send(msg)

if __name__=="__main__":
    cli = Client()
    cli.start()
