# pyright: reportGeneralTypeIssues=false

import socket

class server:
    def __init__(self) -> None:
        self.known_port = 50002
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind(('0.0.0.0', 55555))

    def run(self) -> None:
        while True:
            clients = []

            while True:
                _, address = self.__socket.recvfrom(128)

                print('connection from: {}'.format(address))
                clients.append(address)

                self.__socket.sendto(b'ready', address)

                if len(clients) == 2:
                    print('got 2 clients, sending details to each')
                    break

            c1 = clients.pop()
            c1_addr, c1_port = c1
            c2 = clients.pop()
            c2_addr, c2_port = c2

            self.__socket.sendto('{} {} {}'.format(c1_addr, c1_port, self.known_port).encode(), c2)
            self.__socket.sendto('{} {} {}'.format(c2_addr, c2_port, self.known_port).encode(), c1)

if __name__ == '__main__':
    server = server()
    server.run()
