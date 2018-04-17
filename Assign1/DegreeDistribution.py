import AbstractNetwork
class DegreeDistribution:
    """Calculates a degree distribution for a network"""

    def __init__(self, network):
        """
        Inits DegreeDistribution with a network and calculate its distribution
        """
	self.histogram = [0] * network.maxDegree()
	for i in range(0, network.size()):
		self.histogram[network.getNode(i).degree()] += 1
    	getNormalizedDistribution()

    def getNormalizedDistribution(self):
        '''
        Returns the computed normalized distribution
        '''
	for i in range(0, network.maxDegree()):
		self.histogram /= network.size()
