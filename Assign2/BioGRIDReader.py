from os.path import exists
from sets import Set

class BioGRIDReader:
    '''Reads BioGRID tab files'''
    def __init__(self, filename):
        '''
        Initialization, read in file and build any data structure that makes you happy
        '''
        # Use dic of Sets of Tuples
        self.storage = dict()
        if exists(filename):
            # "with" closes the file again after reading 
            with open(filename) as openfile:
                # catch table header line
                first = True
                for line in openfile:
                    # get entries of a line as list
                    content = self.separate(line[0:(len(line)-1)])
                    # and store them
                    if first:
                        first = False
                    else:
                        self.store(content)
        else:
            print filename, "does not exist"

    def separate(self, line):
        '''
        Split line into list of entries
        '''
        if "\t" in line:
            content = line.split("\t")
            return content
        # return empty list if not splitable
        return []

    def store(self, content):
        '''
        Store content of a line in the dict structure
        '''
        # check validity of input
        if len(content) == 11:
            # check if both genes are from the same organism
            if content[9] == content[10]:
                # extract important information
                organism = content[9]
                geneA = content[0]
                geneB = content[1]
                # store the results
                if self.storage.has_key(organism): 
                    self.storage[organism].add((geneA, geneB))
                    # avoid reverse duplicated for non-self-loops
                    if geneA != geneB:
                        self.storage[organism].discard((geneB, geneA))
                else:
                    # use a set, it avoids duplicates
                    self.storage[organism] = Set()
                    self.storage[organism].add((geneA, geneB))

    def getInteractions(self, taxonID):
        '''
        Return the number of links between genes of a prganism
        '''
        return self.storage[taxonID]
	
    def getMostAbundantTaxonIDs(self, n):
        '''
        Returns a list of n (taxonID/number of links) lists with
        the most reported genes interactions per organisms 
        '''
        # allow bad paraeters to be handled
        if n > len(self.storage):
            n = len(self.storage)
        if n < 0:
            n = 0
        # use lefmade sort algorithm
        # iterate over organisms and store the number of interaction
        # use a decreasing order
        counter = []
        first = True
        for i in self.storage.keys():
            links = len(self.storage[i])
            inserted = False
            # first element must be inserted
            if first:
                counter.append([i, links])
                first = False
            else:
                # find position for insertion
                for j in range(0,len(counter)):
                    if links > counter[j][1]:
                        counter.insert(j,[i, links])
                        inserted = True
                        break
                if not inserted:
                    counter.append([i, links])
        # return the required n organisms with the most interactions
        return counter[0:n]

