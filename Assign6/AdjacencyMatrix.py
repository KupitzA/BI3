class AdjacencyMatrix:
	"""
	Adjancency matrix, encoding a squared matrix with edge weight
	information between nodes.
	Initilialization and data access is only possible over the
	row and column lables, not by positions
	"""
	
	def __init__(self, initial, lables):
		"""
		Initialization of the adjacency matrix, required are an
		initial default weight and row lables, which are also used as
		column lables -> leading to a squared matrix
		"""
		self.lables = lables
		# default setup
		self.matrix = [0] * len(lables)
		for i in range(0, len(self.matrix)):
			self.matrix[i] = [initial] * len(lables)
		
		# Similar to the state class, data access is only possible
		# with row and column lables, dicts enable an acces in linear
		# time
		self.access = dict()
		counter = 0
		for i in self.lables:
			self.access[i] = counter
			counter += 1
		
	def setByLable(self, a, b, value):
		"""
		Set the weight for the edge from a to b
		"""
		self.matrix[self.access[a]][self.access[b]] = value
	
	def getByLable(self, a, b):
		"""
		Get the weight for the edge from a to b
		"""
		return self.matrix[self.access[a]][self.access[b]]
	
	def size(self):
		"""
		Returns the size of the matrix
		expressed by the number of lables
		"""
		return len(self.lables)
		
	def show(self):
		"""
		Output the matrix as collection of lists
		"""
		print("Square Matrix:")
		for i in range(0, len(self.lables)):
			print(self.matrix[i])
