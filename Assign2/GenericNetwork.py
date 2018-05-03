from os.path import exists
from AbstractNetwork import AbstractNetwork
from BioGRIDReader import BioGRIDReader
from AbstractNetwork import AbstractNetwork
from Node import Node

class GenericNetwork(AbstractNetwork):
    def __init__(self, filename):
        """
        Create a network from a file
        """
        self.nodes = {}
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
            print filename, "does not exist"
        
    
    def printDegreeHigherThan(self, n):
        '''
        Print proteins, with more than n interactions
        '''
        for i in self.nodes:
            if(self.getNode(i).degree() > n):
                print i, self.getNode(i).degree()
                
    def degreeDistribution(self):
        vector = [0.0]*(self.size()+1)
        for name in self.nodes:
            node = self.getNode(name)
            vector[node.degree()] += 1.0
        for i in range(0,len(vector)):
            vector[i] /= float(self.size())
        return vector
