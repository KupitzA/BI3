class State:
	"""
	Encode if genes are active (1) or inactive (0) or inactive
	Covers a simple list and extends it with functionality required
	by the PropagationMatrix and SquareMatrix class
	Data acces can only be done by using the gene lables.
	"""
	
	def __init__(self,lables):
		"""
		Initialize a state with the set of all gene lables
		"""
		self.lables = lables
		# dict allows to access the data by lable in linear time
		self.access = dict()
		counter = 0
		for l in lables:
			self.access[l] = counter
			counter += 1
		# encondes if genes are active or inactive
		self.state = [0] * len(lables)
		
	def setByLable(self, lable, value):
		"""
		Set the gene with a given lable avtive or inactive
		Every input will be translated to active (1) or inactive (0)
		"""
		self.state[self.access[lable]] = 0 if value <= 0 else 1
		
	def getByLable(self, lable):
		"""
		Returns 1 if the gene with a certain lable is active,
		0 otherwise
		"""
		return self.state[self.access[lable]]
	
	def getLables(self):
		"""
		Returns the lables of genes
		"""
		return self.lables
		
	def size(self):
		"""
		Returns the lenght of the state,
		i.g. the number of encoded genes
		"""
		return len(self.lables)
	
	def getInt(self):
		"""
		Returns the unique integer obtained by the binary encoded
		genes (active or inactive)
		"""
		value = 0
		for n in range(0,len(self.lables)):
			value += self.state[n] * (2**n)
		return value
	
	def setInt(self, value):
		"""
		Initializes a state whose binary representation equals the
		provided integer value
		"""
		if value == 0:
			return
		binaries = 2**(len(self.lables)-1)
		pos = len(self.lables) - 1
		while pos >= 0:
			if value >= binaries:
				self.state[pos] = 1
				value -= binaries
			binaries /= 2
			pos -= 1
		return
	
	def show(self):
		"""
		Output the state as binary list
		"""
		print("State:")
		print(self.state)
