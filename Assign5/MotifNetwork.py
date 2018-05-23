import random
from CliqueNetwork import CliqueNetwork


class MotifNetworks:
    """
    class that takes a parameter n and a network and computes if cliques of size 3, 4 and 5 are significantly (p < 0:05)
     enriched in that network
    """
    network = CliqueNetwork("", "")
    clique = list()

    def __init__(self, network, n):
        self.network = network
        #compute number of cliques in original network
        self.clique = self.network.findCliques()
        #perform n switches
        cliques = self.__createNetwork__(n)
        c_i = dict()
        #initilize dict
        for i in range(3, 6):
                c_i[i] = 0
        #count cliques of size i
        for i in self.clique:
            c_i[len(i)] = c_i.get(len(i), 0) + 1
        # count cliques of size of at least i
        for i in range(4, 2, -1):
                c_i[i] += c_i[i+1]
        #compute p_i
        extremes = list()
        for key, item in c_i.items():
            extremes.append((key, self.count(cliques, key, item)))
        print(extremes)


    def __createNetwork__(self, n):
        """
        for 2m iterations, randomly select two edges e1 = (n1; n2) and e2 = (n3; n4) from the network and rewire them
        such that the start and end nodes are swapped
        :param n: number of swaps
        """
        cliques = list()
        for i in range(n):
            node1 = self.chooseNode()
            node2 = random.choice(node1.nodelist)
            node3 = self.chooseNode()
            node4 = random.choice(node3.nodelist)
            node1.addLinkTo(node4)
            node3.addLinkTo(node2)
            node1.removeLinkTo(node2)
            node3.removeLinkTo(node4)
            clique = self.network.findCliques()
            cliques.append(clique)
        return cliques

    def count(self, cliques, i, c_i):
        """
        count cliques of size of at least i
        :param cliques: randomized cliques
        :param i: clique size
        :param c_i: number of cliques with clique size of at least i in original network
        :return: number of networks with at least as many cliques of size of at least i over number of randomized
                networks
        """
        extremes = 0
        for network in cliques:
            count = 0
            for clique in network:
                if len(clique) >= i:
                    count += 1
            if count >= c_i:
                extremes += 1
        extremes /= float(len(cliques))
        return extremes

    def chooseNode(self):
        """
        choose random node with edges
        :return: random node with at least one edge
        """
        nodeid = random.choice(list(self.network.nodes))
        node = self.network.nodes[nodeid]
        if len(node.nodelist) != 0:
            return node
        else:
            self.chooseNode()


cn = CliqueNetwork("rat_network.tsv", "dummy")
MotifNetworks(cn, 100)
