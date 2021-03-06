import matplotlib.pyplot as plt
import math

def plotDistributionComparison(histograms, legend, title):
    '''
    Plots a list of histograms with matching list of descriptions as the legend
    '''
    # determine max. length
    max_length = max(len(x) for x in histograms)
    
    # extend "shorter" distributions
    for x in histograms:
        x.extend([0.0]* (max_length-len(x)) )
        
    # plots histograms
    for h in histograms:
        plt.plot(range(len(h)), h, marker = 'x')
    
    # remember: never forget labels!
    plt.xlabel('degree')
    plt.ylabel('P')
    
    # you don't have to do something stuff here
    plt.legend(legend)
    plt.title(title)
    plt.tight_layout()
    plt.show()

def plotDistributionComparisonLogLog(histograms, legend, title):
    '''
    Plots a list of histograms with matching list of descriptions as the legend
    '''
    ax = plt.subplot()
    # determine max. length
    max_length = max(len(x) for x in histograms)
    
    # extend "shorter" distributions
    for x in histograms:
        x.extend([0.0]* (max_length-len(x)) )
    
    ax.set_xscale("log")  
    ax.set_yscale("log")
      
    # plots histograms
    for h in histograms:
        ax.plot(range(len(h)), h, marker = 'x', linestyle='')
    
    # remember: never forget labels!
    plt.xlabel('degree')
    plt.ylabel('P')
    
    # you don't have to do something stuff here
    plt.legend(legend)
    plt.title(title)
    plt.tight_layout()
    plt.show()
    
def getScaleFreeDistributionHistogram(gamma, k):
    '''
    Generates a Power law distribution histogram with slope gamma up to degree k
    '''
    histogram = list()
    histogram.append(0)
    for i in range(1, k):
        histogram.append(1.0 / math.pow(i, gamma))
    return histogram
    

def simpleKSdist(histogram_a, histogram_b):
    '''
    Simple Kolmogorov-Smirnov distance implementation
    '''
    dist = list()
    F1 = {0: histogram_a[0]}
    F2 = {0: histogram_b[0]}
    for x in range(1, len(histogram_a)):
        F1[x] = F1[x-1] + histogram_a[x]
        F2[x] = F2[x - 1] + histogram_b[x]
        dist.append(abs(F1[x] - F2[x]))
    return max(x for x in dist)
    
def poisson(k, l):
    '''
    Compute the poisson entry for k and lambda (l)
    '''
    k = float(k)
    l = float(l)
    if (k == 0):
        return(math.exp(-1.0*l))
    else:
        return (l/k)*poisson(k-1.0,l)

def getPoissonDistributionHistogram(num_nodes, num_links, k):
    '''
    Generates a Poisson distribution histogram up to k
    '''
    poissonHist = []	
    lambda_ = 2.0*(float(num_links))/float(num_nodes)
    print "Lambda:", lambda_
    for i in range(0,num_links):
	if(i <= k):
		poissonHist.append(poisson(i, lambda_))
    return poissonHist

