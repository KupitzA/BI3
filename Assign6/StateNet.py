class Node:
	def __init__(self, index):
		self.id = index
		self.orbit = 0
	
	def addLinkTo(self, index):
		self.linkto = index

	def getLink(self):
		return self.linkto
	
	def setOrbit(self, number):
		self.orbit = number
	
	def getOrbit(self, number):
		return self.orbit
		
class StateNet:
	def __init__(self, num_nodes):
		self.nodes = dict()
		for i in range(0,num_nodes):
			self.nodes[i] = [Node(i), 0]
	
	def addEdge(self, index1, index2):
		self.nodes[index1][0].addLinkTo(index2)
		self.nodes[index2][1] += 1
	
	#def assignOrbits(self):
	#	for idx in self.nodes.getKeys():
	#		if self.nodes[idx][0].getOrbit() == 0:
				
	
	def getNode(self, index):
		return self.nodes[index][0]
	
	def getIndegree(self, index):
		return self.nodes[index][1]
		
	def getKeys(self):
		return self.nodes.keys()
	
	def show(self):
		print(self.nodes)
