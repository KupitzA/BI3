from BioGRIDReader import BioGRIDReader
from GenericNetwork import GenericNetwork
from DegreeDistribution import DegreeDistribution
import Tools

#read in Grid
reader = BioGRIDReader("BIOGRID-ALL-3.4.159.tab.txt")

#printed as list of lists, first 
print reader.getMostAbundantTaxonIDs(5)

# write file for generic network
reader.writeInteractionFile("9606", "human.txt")
net = GenericNetwork("human.txt")

# get distribution of current network
dist = DegreeDistribution(net).getNormalizedDistribution()
# get poisson
# properties:
nodes = net.size()
links = 275472
poisson = Tools.getPoissonDistributionHistogram(nodes, links, 100)
sf = Tools.getScaleFreeDistributionHistogram(0.5, 100)
Tools.plotDistributionComparison([dist, poisson, sf],["human interaction network", "poisson distribution", "scale free distribution"], "teste")
