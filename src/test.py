from pythonp2p import Node

def generateNode(base=2):
    try:
        return Node('0.0.0.0', base )
    except :
        return generateNode(base+1)


node = generateNode()
print(node)
node.start()

