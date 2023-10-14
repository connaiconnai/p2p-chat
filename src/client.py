# pyright: reportGeneralTypeIssues=false

import socket
import threading

rendezvous = ('0.0.0.0', 55555)

class client:
    def __init__(self, port) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind(('0.0.0.0', int(port)))
        self.__socket.sendto(b'0', rendezvous)

        while True:
            data = self.__socket.recv(1024).decode()
            if data.strip() == 'ready':
                print('checked in with server, waiting')
                break

        data = self.__socket.recv(1024).decode()
        self.ip, sport, dport = data.split(' ')
        self.sport = int(sport)
        self.dport = int(dport)

    def listen(self):
        while True:
            data = self.__socket.recv(1024)
            print('\rpeer: {}\n> '.format(data.decode()), end='')


    def run(self):
        print('\ngot peer')
        print('  ip:          {}'.format(self.ip))
        print('  source port: {}'.format(self.sport))
        print('  dest port:   {}\n'.format(self.dport))

        # equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
        print('punching hole')
        print('ready to exchange messages\n')

        listener = threading.Thread(target=self.listen, daemon=True);
        listener.start()

        while True:
            msg = input('> ')
            self.__socket.sendto(msg.encode(), (self.ip, self.sport))


if __name__ == '__main__':
    port = input('port: ')
    client = client(port)
    client.run()
