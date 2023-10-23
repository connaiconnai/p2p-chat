from Node import Node


def generateNode(base=2):
    try:
        return Node('0.0.0.0', base)
    except :
        return generateNode(base+1)


node = generateNode()
node.start()

try:
    if(node.port > 2):
        # host and port for test
        host = node.host
        port = "2"
        node.connect_to(host, int(port))
    while not node.terminate_flag.is_set():
        msg = input("msg: ")
        node.message(msg)

        if(msg == "q"):
            node.stop()
            break

except Exception as e:
    print(e)
    node.stop()
