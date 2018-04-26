from ScaleFreeNetwork import ScaleFreeNetwork
from RandomNetwork import RandomNetwork
import Tools
import numpy as np


def computeDegreeDistribution(AbstractNetwork):
    """
    Inits DegreeDistribution with a network and calculate its distribution
    """
    # one further entry since 0 is degree 0 is included
    histogram = [0.0] * (AbstractNetwork.maxDegree() + 1)
    # increment degree distribution
    for i in range(0, AbstractNetwork.size()):
        histogram[AbstractNetwork.getNode(i).degree()] += 1.0
    # turn it into a real distribution
    for i in range(0, len(histogram)):
        histogram[i] /= float(AbstractNetwork.size())
    return histogram


def comparison1():
    net1 = ScaleFreeNetwork(1000, 2)
    net2 = ScaleFreeNetwork(10000, 2)
    hist1 = computeDegreeDistribution(net1)
    hist2 = computeDegreeDistribution(net2)
    histograms = list()
    legend = list()
    histograms.append(hist1)
    legend.append("network with 1000 nodes")
    histograms.append(hist2)
    legend.append("network with 10000 nodes")
    Tools.plotDistributionComparisonLogLog(histograms, legend, "Task 1 b)")


def comparison2():
    net1 = ScaleFreeNetwork(1000, 2)
    net2 = RandomNetwork(1000, 2)
    hist1 = computeDegreeDistribution(net1)
    hist2 = computeDegreeDistribution(net2)
    histograms = list()
    legend = list()
    histograms.append(hist1)
    legend.append("scale-free network")
    histograms.append(hist2)
    legend.append(" random network")
    Tools.plotDistributionComparisonLogLog(histograms, legend, "Task 1 b)")


def determineGamma():
    net1 = ScaleFreeNetwork(10000, 2)
    hist1 = computeDegreeDistribution(net1)
    mindist = float("inf")
    bestgamma = 0
    for gamma in np.arange(1, 3, 0.1):
        hist2 = Tools.getScaleFreeDistributionHistogram(gamma, 10000)
        dist = Tools.simpleKSdist(hist1, hist2)
        if dist < mindist:
            mindist = dist
            bestgamma = gamma
    histograms = list()
    histograms.append(hist1)
    histograms.append(hist2)
    legend = list()
    legend.append("empirical distribution")
    histograms.append("optimal distribution")
    Tools.plotDistributionComparisonLogLog(histograms, legend, "Task 1 c)")
    return bestgamma


determineGamma()
#comparison2()

