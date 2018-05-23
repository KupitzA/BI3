from AbstractNetwork import AbstractNetwork
import random

from CliqueNetwork import CliqueNetwork


class RandomizedNetwork(AbstractNetwork):
    def __createNetwork__(self, network, m):
        self.nodes = network.nodes
        for i in range(2*m):
            node1id = random.choice(list(self.nodes))
            node1 = self.nodes[node1id]
            node2 = random.choice(node1.nodelist)
            node3id = random.choice(list(self.nodes))
            node3 = self.nodes[node3id]
            node4 = random.choice(node3.nodelist)
            node1.addLinkTo(node4)
            node3.addLinkTo(node2)
            node1.removeLinkTo(node2)
            node3.removeLinkTo(node4)


cn = RandomizedNetwork(CliqueNetwork("test.tsv", "dummy"), 10)
