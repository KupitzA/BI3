from Node import Node

class AbstractNetwork:
    """Abstract network definition, can not be instantiated"""
    
    def __init__(self, amount_nodes, amount_links):
        """
        Creates empty nodelist and call createNetwork of the extending class
        """
        self.nodes = {}
        self.__createNetwork__(amount_nodes, amount_links)

    def __createNetwork__(self, amount_nodes, amount_links):
        """
        Method overwritten by subclasses, nothing to do here
        """
        raise NotImplementedError

    def appendNode(self, node):
        """
        Appends node to network
        """
        self.nodes[node.id] = node

    def maxDegree(self):
        """
        Returns the maximum degree in this network
        """
        maxdegree = 0
        for n in self.nodes.itervalues():
            if maxdegree < n.degree():
                maxdegree = n.degree()
        return maxdegree

    def size(self):
        """
        Returns network size (here: number of nodes)
        """
        return len(self.nodes)

    def __str__(self):
        '''
        Any string-representation of the network (something simply is enough)
        '''
        for n in self.nodes.itervalues():
            for ref in range(n.id,len(n.nogelist())):
                println(n + " - " + ref)

    def getNode(self, identifier):
        """
        Returns node according to key
        """
        return self.nodes[identifier]
