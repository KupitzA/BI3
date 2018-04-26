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
        linksPerIteration = (amount_links-3)/(amount_nodes-3) if amount_nodes > 3 else 1
        #generate n nodes
        while numOfNodes < amount_nodes:
            node = Node(numOfNodes)
            self.appendNode(node)
            numOfNodes += 1
            #make first three nodes fully connected
            if numOfNodes == 2:
                self.__connectNode__(numOfNodes, 1)
            if numOfNodes == 3:
                self.__connectNode__(numOfNodes, 2)
            #link following nodes
            if numOfNodes > 3:
                self.__connectNode__(numOfNodes, linksPerIteration)

    def __connectNode__(self, numOfNodes, linksPerIteration):
        """
        Connect an existing node to m other nodes
        :param numOfNodes: current amount of nodes
        :param linksPerIterations: number of links that should be added in this iteration
        """
        numOfLinks = 0
        # add n links per iteration
        while numOfLinks < linksPerIteration:
            #choose second node randomly
            nodeid2 = random.randint(0, numOfNodes-2)
            node1 = self.getNode(numOfNodes-1)
            node2 = self.getNode(nodeid2)
            if not node1.hasLinkTo(node2):
                #determine probability to choose node
                if self.degreeSum != 0 and node2.degree() != 0:
                    pi = float(node2.degree()) / self.degreeSum
                else:
                    pi = float(1)
                r = random.random()
                #choose node with probability pi
                if r < pi:
                    numOfLinks += 1
                    self.degreeSum += 2
                    node1.addLinkTo(node2)
                    node2.addLinkTo(node1)
