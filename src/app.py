from Server import Server
from Client import Client


port = int(input("binding port >"))
server = Server(port)
server.start()

# host and port for test
client = Client()
client.connection()
client.message()
