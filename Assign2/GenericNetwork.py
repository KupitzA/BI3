from os.path import exists
from AbstractNetwork import AbstractNetwork
from BioGRIDReader import BioGRIDReader
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
