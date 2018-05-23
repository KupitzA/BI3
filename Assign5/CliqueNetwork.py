import random
from os.path import exists
from AbstractNetwork import AbstractNetwork
import matplotlib.pyplot as plt


class CliqueNetwork(AbstractNetwork):
    """
    function that computes the number of cliques of sizes 3, 4 and 5 in a network
    """
    def __createNetwork__(self, filename, dummy):
        """
        Create a network from a file
        """
        if exists(filename):
            # "with" closes the file again after reading 
            with open(filename) as openfile:
                for line in openfile:
                    # get entries of a line as list
                    content = line[0:(len(line)-1)].split("\t")
                    # and store them
                    if len(content) == 2:
                        n1 = self.getNode(content[0])
                        n2 = self.getNode(content[1])
                        n1.addLinkTo(n2)
                        n2.addLinkTo(n1)
        else:
            print(filename, "does not exist")

    def findCliques(self):
        """
        function that computes the number of cliques of sizes 3, 4 and 5 in a network.
        :return: list of cliques
        """
        cliques = []
        for node1 in self.nodes.values():
            for node2 in node1.nodelist:
                candidates = list()
                candidates.append(node1)
                candidates.append(node2)
                clique = set(self.extendClique(candidates, 3))
                #only consider cliques of size 3-5
                if clique not in cliques and len(clique) > 2:
                    cliques.append(clique)
        return cliques

    def extendClique(self, candidates, depth):
        """
        try to extend clique to larger cliques
        :param candidates: smaller clique
        :param depth: clique size; maximal 5
        :return: largest clique possible
        """
        if depth <= 5:
            for nextnode in candidates[0].nodelist:
                if nextnode not in candidates:
                    #check if node is connected to all nodes in clique
                    if all(nextnode.hasLinkTo(x) for x in candidates):
                        candidates.append(nextnode)
                        self.extendClique(candidates, depth+1)
                    else:
                        return candidates
            return candidates
        else:
            return candidates

    def evolve(self, t):
        """
        function that takes a parameter t representing the number of time steps, as well as a network; for each time
        step, randomly insert or delete one edge in the network
        :param t: number of time steps
        """
        cliques = list()
        for c in range(3):
            cliques.append(t * [0])
        for i in range(t):
            clique = cn.findCliques()
            r = random.random()
            node1id = random.choice(list(self.nodes))
            node1 = self.nodes[node1id]
            #decide if edge gets removed or new edge added
            if r <= 0.5:
                #try to find two nodes without edge
                while True:
                    node2id = random.choice(list(self.nodes))
                    node2 = self.nodes[node2id]
                    if not node1.hasLinkTo(node2):
                        node1.addLinkTo(node2)
                        node2.addLinkTo(node1)
                        break
            else:
                #search for edge
                while len(node1.nodelist) == 0:
                    node1id = random.choice(list(self.nodes))
                    node1 = self.nodes[node1id]
                node2 = random.choice(node1.nodelist)
                node1.removeLinkTo(node2)
            #plot number of cliques of size 3, 4 and 5 at the beginning and after each time step as a function of time
            #  with t = 100
            cliques = self.plot(clique, i, cliques)
        for index, item in enumerate(cliques):
            plt.plot(range(len(item)), item, marker='x')
            plt.xlabel('t')
            plt.ylabel('amount of cliques')
            plt.title('Evolving Networks')
            plt.legend('345')
            plt.tight_layout()
        plt.show()
                    
    def printClique(self, clique):
        """
        print cliques to check result
        :param clique: clique to print
        """
        for line in clique:
            s = ''
            for c in line:
                s += str(c)
            print(s)

    def plot(self, clique, t, cliques):
        """
        count amount of cliques of size i at time step t
        :param clique: cliques in current time step
        :param t: time step
        :param cliques: matrix to store count
        :return: matrix with counts
        """
        for c in clique:
            cliques[len(c)-3][t] = cliques[len(c)-3][t] + 1
        return cliques


cn = CliqueNetwork("rat_network.tsv", "dummy")
clique = cn.findCliques()
cn.evolve(1000)
clique = cn.findCliques()
