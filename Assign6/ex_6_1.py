from PropagationMatrix import PropagationMatrix
from State import State

def trackPropagation(state, repeats):
	"""
	Visualize the propagations by a sequence of integers
	"""
	track = str(state.getInt())
	for i in range(1, repeats):
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
print("                        Exercise 6.1 b)                        ")
print("███████████████████████████████████████████████████████████████")
print("\nInitial state 1:")
state_a.setInt(1)
trackPropagation(state_a, 8)

# initialize with the state integer 13
print("\nInitial state 4:")
state_b = State(['A','B','C','D','E','F'])
state_b.setInt(4)
trackPropagation(state_b, 5)

# initialize with the state integer 13
print("\nInitial state 21:")
state_c = State(['A','B','C','D','E','F'])
state_c.setInt(21)
trackPropagation(state_c, 11)

# initialize with the state integer 13
print("\nInitial state 33:")
state_d = State(['A','B','C','D','E','F'])
state_d.setInt(33)
trackPropagation(state_d, 7)

print()
print("                        Exercise 6.1 c)                        ")
print("███████████████████████████████████████████████████████████████")
orbits = prop.orbit()
for i in range(0, len(orbits)):
	print()
	length = len(orbits[i][1])
	print("Orbit " + str(i + 1) + " with length " + str(length) + ":")
	print(orbits[i][1])
	print("Set of basins:")
	print(orbits[i][0])
	coverage = float(len(orbits[i][0]))
	coverage /= float(2**prop.size())
	coverage *= 100.0
	print("Relative coverage: " + str(coverage) + "%")

