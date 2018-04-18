import AbstractNetwork
class DegreeDistribution:
    """Calculates a degree distribution for a network"""

    def __init__(self, network):
        """
        Inits DegreeDistribution with a network and calculate its distribution
        """
	# one further entry since 0 is degree 0 is included
	self.histogram = [0.0] * (network.maxDegree()+1)
	# increment degree distribution
	for i in range(0, network.size()):
		self.histogram[network.getNode(i).degree()] += 1.0
	# turn it into a real distribution
	print self.histogram
	for i in range(0, len(self.histogram)):
		self.histogram[i] /= float(network.size())

    def getNormalizedDistribution(self):
        '''
        Returns the computed normalized distribution
        '''
	return self.histogram
