from Node import Node
from AbstractNetwork import AbstractNetwork 
from RandomNetwork import RandomNetwork 
from DegreeDistribution import DegreeDistribution
from Tools import *

# main properties
numnodes = 5
numedges = 4

network = RandomNetwork(numnodes, numedges)
distObject = DegreeDistribution(network)
distNetwork = distObject.getNormalizedDistribution()

bilderbuch = getPoissonDistributionHistogram(numnodes, numedges, 5)
plotDistributionComparison([distNetwork, bilderbuch], ["Net", "Ref"], "Two ref")
