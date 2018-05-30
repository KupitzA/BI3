from PropagationMatrix import PropagationMatrix
from State import State

def trackPropagation(state):
	"""
	Visualize the propagations by a sequence of integers
	"""
	track = str(state.getInt())
	for i in range(1, 20):
		state = prop.propagate(state)
		track += " -> "
		track += str(state.getInt())
	print(track)

# Initialize propagation network  with text file
# File contains structural informations of the given
# gene regulatory network
prop = PropagationMatrix("net.txt")

# initialize with the state integer 13
state_a = State(['A','B','C','D','E','F'])
state_a.setInt(1)
trackPropagation(state_a)

# initialize with the state integer 13
state_b = State(['A','B','C','D','E','F'])
state_b.setInt(4)
trackPropagation(state_b)

# initialize with the state integer 13
state_c = State(['A','B','C','D','E','F'])
state_c.setInt(21)
trackPropagation(state_c)

# initialize with the state integer 13
state_d = State(['A','B','C','D','E','F'])
state_d.setInt(33)
trackPropagation(state_d)

prop.createStateNetwork()
print(prop.attractors())

