import threading
import socket
from lib import crypto_funcs as cf
from connectionNode import ConnectionNode

MAX_NODE = 10
BUFFER = 4096 # byte
SET_TIMEOUT = 1.0
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

            except:
                pass

    def connect_to(self, host, port=PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        sock.send(self.id.encode("utf-8"))
        connected_node_id = sock.recv(BUFFER).decode("utf-8")
        self.node = sock

        # NOTE: Are there times when connected_node_id is not the same as self.id?
        # if self.id == connected_node_id:
        #     if ipaddress.ip_address(host).is_private:
        #         self.local_ip = host
        #     else:
        #         self.ip = host
        #     self.banned.append(host)
        #     sock.close()
        #     return False

        node = self.create_new_connection(
            sock, connected_node_id, host, port
        )
        self.append_peer(node)

    def create_new_connection(self, sock, id, host, port):
        node = ConnectionNode(self, sock, id, host, port)
        node.start()
        return node

    def append_peer(self, node):
        if node.host not in self.peers:
            self.peers.append(node)
        # self.send_peers()

    def send_to_peers(self, message):
        for i in self.peers:
            i.send(message)

    # TODO: send a message
    def message(self, data):
        self.node.send(data.encode("utf-8"))
        # self.send_to_peers(data.encode("utf-8"))



