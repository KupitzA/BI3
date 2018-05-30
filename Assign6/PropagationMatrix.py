from os.path import exists
from AdjacencyMatrix import AdjacencyMatrix
from State import State

class PropagationMatrix:
	"""
	Implements a propagation matrix. The propagated states are not
	preprocessed and are computed on demand to reduce the required
	amount of memory. Thereby increased runtime-changes are negligible
	"""
	def __init__(self, filename):
		"""
		Create a class object behaving lika a propagation matrix
		for a gene network obtained by textfile
		Textfile specification:
		A > B indicates that gene A turns gene B activate
		A | B indicates that gene A turns gene B inactive
		(space separated)
		"""
		# temporary storage for gene lables (to avoid redundancy)
		nodes = set()
		# temporary storage for linkages (to avoid double file reading)
		links = list()
		if exists(filename):
			with open(filename) as openfile:
				for line in openfile:
					content = line[0:(len(line)-1)].split(" ")
					nodes.add(content[0])
					nodes.add(content[2])
					if (content[1] == ">"):
						links.append((content[0], content[2], 1))
					elif (content[1] == "|"):
						links.append((content[0], content[2], -3))
			
			# sort genes in alphabetiv order by
			# by making use of list functionalities
			nodes = list(nodes)
			nodes.sort()
			
			# initialize a adjacency matrix representing the obtained
			# gene network
			self.matrix = AdjacencyMatrix(0, nodes)
			for triple in links:
				self.matrix.setByLable(triple[0], triple[1], triple[2])
		else:
			print(filename, "does not exist")
		
	def propagate(self, state):
		"""
		Derive the propagated state form a given state
		Each gene is set inactive if the scalar product
		of the given state and its column in the adjacency matrix
		is smaller or equal to zero. Otherwise, the gene is set active
		"""
		prop_state = State(state.getLables())
		for lab_y in state.getLables():
			# scalar product
			temp = 0
			for lab_x in state.getLables():
				temp += state.getByLable(lab_x) * self.matrix.getByLable(lab_x, lab_y)
			# threshold task specific
			prop_state.setByLable(lab_y, 0 if temp <= 0 else 1)
		return prop_state
