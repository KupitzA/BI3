from AbstractNetwork import AbstractNetwork
import random

from CliqueNetwork import CliqueNetwork


class RandomizedNetwork(AbstractNetwork):
    """
    function that takes a network with m edges and returns a randomised version of that network
    """
    def __createNetwork__(self, network, m):
        """
        for 2m iterations, randomly select two edges e1 = (n1; n2) and e2 = (n3; n4) from the network and rewire them
        such that the start and end nodes are swapped
        :param network: network
        :param m: number of edges
        """
        self.nodes = network.nodes
        for i in range(2*m):
            node1 = self.chooseNode()
            node2 = random.choice(node1.nodelist)
            node3 = self.chooseNode()
            node4 = random.choice(node3.nodelist)
            node1.addLinkTo(node4)
            node3.addLinkTo(node2)
            node1.removeLinkTo(node2)
            node3.removeLinkTo(node4)

    def chooseNode(self):
        """
        choose random node with edges
        :return: random node with at least one edge
        """
        nodeid = random.choice(list(self.nodes))
        node = self.nodes[nodeid]
        if len(node.nodelist) != 0:
            return node
        else:
            self.chooseNode()


cn = RandomizedNetwork(CliqueNetwork("test.tsv", "dummy"), 10)
