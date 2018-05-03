from BioGRIDReader import BioGRIDReader
from AbstractNetwork import AbstractNetwork
from GenericNetwork import GenericNetwork
#from DegreeDistribution import DegreeDistribution
import Tools

#read in Grid
reader = BioGRIDReader("BIOGRID-ALL-3.4.159.tab.txt")

#printed as list of lists, first 

# write file for generic network
reader.writeInteractionFile("9606", "human.txt")
net = GenericNetwork("human.txt")
#net.printDegreeHigherThan(1000)
#print net.getNode("ETG7706").degree()
#print net.getNode("ETG7157").degree()
# get distribution of current network
dist = net.degreeDistribution()
#print dist[0:20]
# get poisson
# properties:
nodes = net.size()
links = 275472
poisson = Tools.getPoissonDistributionHistogram(nodes, links, 100)
sf = Tools.getScaleFreeDistributionHistogram(0.1, 100)
Tools.plotDistributionComparison([dist[0:100], poisson, sf],["Human interaction network", "Poisson distribution", "Scale-free distribution"], "Distribution")

