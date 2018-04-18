from Node import Node
from AbstractNetwork import AbstractNetwork 
from RandomNetwork import RandomNetwork 
from DegreeDistribution import DegreeDistribution
from Tools import *

# main properties
numnodes = 100
numedges = 300

network = RandomNetwork(numnodes, numedges)
distObject = DegreeDistribution(network)
distNetwork = distObject.getNormalizedDistribution()

distributions = []
distributions.append(distNetwork)
distributions.append(getPoissonDistributionHistogram(numnodes, numedges, 10))
names = ["REAL", "POISSON"]
plotDistributionComparison(distributions, names, "Two ref")

