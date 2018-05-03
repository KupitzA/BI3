from AbstractNetwork import AbstractNetwork
from Node import Node
import random # you will need it :-)

class RandomNetwork(AbstractNetwork):
    """Random network implementation of AbstractNetwork"""
    
    def __createNetwork__(self, amount_nodes, amount_links): # remaining methods are taken from AbstractNetwork
        """
        Creates a random network
        1. Build a list of n nodes
        2. For i=#links steps, add a connection between for two randomly chosen nodes that are not yet connected
        """
        for nodeid in range(0, amount_nodes):
            n = Node(nodeid)
            self.appendNode(n)

        random.seed()
        if amount_nodes > 1:
            p = 2*amount_links/(amount_nodes*(amount_nodes-1))
        else:
            p = 0

        links = 0
        while links < amount_links:
            randint1 = random.randint(0,len(self.nodes)-1)
            randint2 = random.randint(0,len(self.nodes)-1)
            n1 = self.getNode(randint1)
            n2 = self.getNode(randint2)
            if randint1 != randint2:
                if n1.addLinkTo(n2):
                    links += 1
                    n2.addLinkTo(n1)
