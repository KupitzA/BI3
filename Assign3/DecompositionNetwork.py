from os.path import exists
from AbstractNetwork import AbstractNetwork
from AbstractNetwork import AbstractNetwork
from Node import Node

class DecompositionNetwork(AbstractNetwork):
    def __createNetwork__(self, filename, dummy):
        """
        Create a network from a file
        """
        self.edgematrix = []
        self.nodeIDs = dict()
        self.count = 0  # count names
        self.num_edges = 0
        names = []
        if exists(filename):
            # "with" closes the file again after reading 
            with open(filename) as openfile:
                for line in openfile:
                    # get entries of a line as list
                    content = line[0:(len(line)-1)].split(" ")
                    # and store them
                    if len(content) == 2:
                        n1 = self.getNode(content[0])
                        n2 = self.getNode(content[1])
                        n1.addLinkTo(n2)
                        n2.addLinkTo(n1)
                        self.num_edges += 1
                        # store names and positions for later access
                        if content[0] not in names:
                            names.append(content[0])
                            self.nodeIDs[self.count] = content[0]
                            self.count += 1
                        if content[1] not in names:
                            names.append(content[1])
                            self.nodeIDs[self.count] = content[1]
                            self.count += 1
        else:
            print(filename, "does not exist")
     
    def getC(self, node1, node2):
        if self.getNode(node1).hasLinkTo(self.getNode(node2)):
            triangles = 0
            # find triangles
            for i in self.getNode(node1).nodelist:
                for j in i.nodelist:
                    if j.id == node2:
                        triangles += 1
                        break
            # get minimal degree
            min_degree = self.getNode(node1).degree()
            if min_degree > self.getNode(node2).degree():
                min_degree = self.getNode(node2).degree()
            # return C + avoid errors
            if min_degree > 1:
                return float(triangles+1)/float(min_degree-1)
            else:
                return 0.0
        else:
            return 3.0
       
    def updateEdgeMatrix(self):
        """
        compute scores clustering coefficients for each edge
        """
        self.edgematrix = []
        for i in range(0,self.size()):
            self.edgematrix.append([3.0]*self.size())
        for i in range(0,self.size()):
            for j in range(0,self.size()):
                name1 = self.nodeIDs[i]
                name2 = self.nodeIDs[j]
                self.edgematrix[i][j] = self.getC(name1, name2)
    
       
    def deleteOneEdge(self):
        """
        Delete the edge with the smalest clustering coefficient
        """
        min_x = ""
        min_y = ""
        min_v = 3
        # serch in materix
        for i in range(0,self.size()):
            for j in range(i,self.size()):
                if self.edgematrix[i][j] < min_v:
                    min_v = self.edgematrix[i][j]
                    min_x = self.nodeIDs[i]
                    min_y = self.nodeIDs[j]
        # remove edge
        self.getNode(min_x).removeLinkTo(self.getNode(min_y))
        self.getNode(min_y).removeLinkTo(self.getNode(min_x))
        self.num_edges -= 1
        print("Remove edge with clustering coefficient", min_v, ":\t", min_x, "-", min_y)
    
    def decomposite(self):
        """
        Controle edge decomposition until each edge is removed
        """
        while self.num_edges > 0:
            self.updateEdgeMatrix()
            self.deleteOneEdge()



