import socket
import threading

rendezvous = ('0.0.0.0', 55555)

# connect to rendezvous
print('connecting to rendezvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', rendezvous)

while True:
    data = sock.recv(1024).decode()
    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')
print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l 50001
def listen():
    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()


while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, sport))
