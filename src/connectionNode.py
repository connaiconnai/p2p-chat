import threading
import socket
import time

# time to disconnect from node if not pinged, nodes ping after 20s
DEAD_TIME = 45
SET_TIMEOUT = 60.0
BUFFER = 4096  # byte


class ConnectionNode(threading.Thread):
    def __init__(self, id, host, port, master_node):
        super(ConnectionNode, self).__init__()
        self.master_node = master_node
        self.id = id
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.settimeout(SET_TIMEOUT)
        self.terminate_flag = threading.Event()
        self.last_ping = time.time()
        # Variable for parsing the incoming json messages
        self.buffer = ""

    def send(self, data):
        try:
            # print(self.sock)
            # print(self.master_node.port, self.master_node.host)
            self.sock.send(data)
        except:
            self.terminate_flag.set()

    def connection_dead(self):
        self.sock.settimeout(None)
        self.sock.close()
        time.sleep(1)

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        while not self.terminate_flag.is_set():
            if time.time() - self.last_ping > DEAD_TIME:
                self.terminate_flag.set()
                print("node" + self.id + "is dead")

            time.sleep(0.1)

        # if running is stop
        self.connection_dead()
