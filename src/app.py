from Node import Node


def generateNode(base=2):
    try:
        return Node('', base)
    except :
        return generateNode(base+1)


node = generateNode()
node.start()

if(node.port > 2):
    try:
        host = "192.168.107.2"
        port = "2"
        node.connect_to(host, int(port))
        while not node.terminate_flag.is_set():
            cmd = input("command: ")
            if(cmd == "connect"):
                pass

            if(cmd == "msg"):
                msg = input("msg: ")
                node.message(msg)

            if(cmd == "q"):
                node.stop()
                break
    except Exception as e:
        print(e)
        node.stop()
