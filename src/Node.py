import threading
import socket
from lib import crypto_funcs as cf
from connectionNode import ConnectionNode

MAX_NODE = 10
BUFFER = 4096 # byte
SET_TIMEOUT = 60.0
PORT = 2

# TODO: port forward
class Node(threading.Thread):
    def __init__(self, host = "0.0.0.0", port = PORT ):
        super(Node, self).__init__()

        self.terminate_flag = threading.Event()

        self.host = host
        self.ip = host
        self.port = port

        hostname = socket.gethostname()
        self.local_ip = socket.gethostbyname(hostname)

        self.publickey, self.private_key = cf.generate_keys()
        self.id = cf.serialize_key(self.publickey)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(SET_TIMEOUT)
        self.sock.listen(1)

        self.peers = []


    def stop(self):
        self.terminate_flag.set()

    # receive connection and message
    # response my id
    def run(self):
        print('IP: ' + str(self.ip))
        print('PORT: ' + str(self.port))
        while(not self.terminate_flag.is_set()):
            try:
                conn, addr = self.sock.accept()
                data = conn.recv(BUFFER).decode("utf-8")
                conn.send(self.id.encode("utf-8"))
                if data:
                    print(data)

            except Exception as e:
                print(e)
                pass

    def connect_to(self, host, port=PORT):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))

            sock.send(self.id.encode("utf-8"))
            connected_node_id = sock.recv(BUFFER).decode("utf-8")
            self.pear = (host, port)

            self.node = self.create_new_connection(
                sock, connected_node_id, host, port
            )
            self.append_peer(self.node)
        except ConnectionResetError as e:
            print(e)
        except BrokenPipeError as e:
            print(e)

    # WARNING: need new socket instance.
    def create_new_connection(self, sock, id, host, port):
        re_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        re_sock.connect((host, port))
        node = ConnectionNode(self, re_sock, id, host, port)
        return node

    def node_connected(self, node):
        if node.host not in self.peers:
            self.peers.append(node.host)
        # self.send_peers()

    def append_peer(self, node):
        if node.host not in self.peers:
            self.peers.append(node)
        # self.send_peers()

    # def send_peers(self):
    #     self.message("peers", self.peers)

    def send_to_peers(self, message):
        for i in self.peers:
            i.send(message)

    # FIX: once send
    def message(self, data):
        try:
            self.send_to_peers(data.encode("utf-8"))
        except Exception as e:
            print(e)



