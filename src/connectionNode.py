import threading
import socket
import time

# time to disconnect from node if not pinged, nodes ping after 20s
DEAD_TIME = ( 45 )
SET_TIMEOUT = 60.0
BUFFER = 4096 # byte

class ConnectionNode(threading.Thread):
    def __init__(self, main_node, sock, id, host, port):
        super(ConnectionNode, self).__init__()

        self.main_node = main_node
        self.id = id
        self.host = host
        self.port = port
        self.sock = sock
        self.sock.settimeout(SET_TIMEOUT)
        self.terminate_flag = threading.Event()
        self.last_ping = time.time()
        # Variable for parsing the incoming json messages
        self.buffer = ""

    # FIX: once sent
    def send(self, data):
        try:
            self.sock.send(data)

        except Exception as e:
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

            line = ""
            try:
                line = self.sock.recv(BUFFER)
            except socket.timeout:
                pass
            except Exception as e:
                self.terminate_flag.set()

            if line != "":
                try:
                    self.buffer += str(line.decode("utf-8"))

                except Exception as e:
                    print("NodeConnection: Decoding line error | " + str(e))

                # Get the messages by finding the message ending -TSN
                index = self.buffer.find("-TSN")
                while index > 0:
                    message = self.buffer[0:index]
                    self.buffer = self.buffer[index + 4 : :]

                    if message == "ping":
                        self.last_ping = time.time()
                    else:
                        self.main_node.node_message(self, message)

                    index = self.buffer.find("-TSN")

            time.sleep(0.1)

        # if running is stop
        self.connection_dead()

