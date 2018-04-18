import matplotlib.pyplot as plt
import math

def plotDistributionComparison(histograms, legend, title):
    '''
    Plots a list of histograms with matching list of descriptions as the legend
    '''
    # adjust size of elements in histogram 
    longest = 0
    # determine longest histogram
    for h in histograms:
        if(len(h) > longest):
            longest = len(h)
    # adapt other histograms
    for h in histograms:
        h.extend([0] * (longest - len(h)))

    # plots histograms
    for h in histograms:
        plt.plot(range(len(h)), h, marker = 'x')
    
    # remember: never forget labels! :-)
    plt.xlabel('')
    plt.ylabel('')
    
    # you don't have to do something here
    plt.legend(legend)
    plt.title(title)
    plt.tight_layout()# might throw a warning, no problem
    plt.show()

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

