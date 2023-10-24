from Server import Server

def generateNode(base=2):
    try:
        return Server('0.0.0.0', base)
    except :
        return generateNode(base+1)


server = generateNode()
server.start()

if(server.port > 2):
    # host and port for test
    host = server.host
    port = "2"
    server.connect_to(host, int(port))
    server.send_message("test")
    while True:
        msg = input('> ')
        server.send_message(msg)



