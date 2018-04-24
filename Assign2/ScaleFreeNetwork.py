import random
from AbstractNetwork import AbstractNetwork
import Tools
from Node import Node

class ScaleFreeNetwork(AbstractNetwork):
    """Scale-free network implementation of AbstractNetwork"""
    degreeSum = 0
          
    def __createNetwork__(self, amount_nodes, amount_links):
        """
        Create a network with an amount of n nodes, add m links per iteration step
        for n nodes:
            for m links:
                link node to other nodes
        """
        random.seed()
        numOfNodes = 0
        while numOfNodes < amount_nodes:
            node = Node(numOfNodes)
            self.appendNode(node)
            numOfNodes += 1
            if numOfNodes in range(2, 4):
                randint1 = random.randint(0, numOfNodes - 1)
                self.__connectNode__(randint1, 3, 1)
            if numOfNodes > 3:
                self.__connectNode__(numOfNodes-1, numOfNodes, amount_links)

    def __connectNode__(self, nodeid1, amount_nodes, amount_links):
        numOfLinks = 0
        #print("n1:" + str(nodeid1))
        while numOfLinks < amount_links:
            nodeid2 = random.randint(0, amount_nodes-1)
            node1 = self.getNode(nodeid1)
            node2 = self.getNode(nodeid2)
            #print(nodeid2)
            if nodeid1 != nodeid2:
                if not node1.hasLinkTo(node2):
                    if self.degreeSum != 0 and node2.degree() != 0:
                        pi = float(node2.degree()) / self.degreeSum
                    else:
                        pi = float(1)
                    r = random.random()
                    #print(pi)
                    if r < pi:
                        numOfLinks += 1
                        self.degreeSum += 2
                        node1.addLinkTo(node2)
                        node2.addLinkTo(node1)
                        #print(str(nodeid1) + " " + str(nodeid2))
