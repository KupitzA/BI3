import csv

class Model:
    """Builds a model. This basically means to determine all necessary priors and likelihoods
     - P(C), P(Si|C)..."""

    def __init__(self):
        """Inits empty list to store classification value and matrix for corresponding feature
        states"""
        self.classifier = []
        self.featureMatrix = []

    def readTSV(self,file):
        """Read tsv-file in and store values"""
        with open(file) as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                self.classifier.append(row[0])
                features = []
                for i in range(1,99):
                    features.append(row[i])
                self.featureMatrix.append(features)

    def classify(self):
        """
        Compute P(C)
        :return: number of occurrences of class=1
        """
        sumc = self.classifier.count("1")
        probc = float(sumc)/(len(self.classifier)-1)
        print("P(C) = " + str(probc))
        print("P(not C) = " + str(1-probc))
        return sumc

    def conditionalProb(self, sumc):
        """
        Compute P(Si|C) for every feature i and state, compute log-likelihood ratio for each Si
        :param sumc: number of occurrences of class=1
        :return: matrix of log-likelihood ratio for each feature and state
        """
        probc = float(sumc) / (len(self.classifier) - 1)
        probFeature = [0]*100
        for i in range(100):
            probFeature[i] = [0]*4
        #count successfull classifications for each feature and state
        for rownumber, rowvalue in enumerate(self.featureMatrix):
            for feature, state in enumerate(rowvalue):
                if self.classifier[rownumber] == "1":
                    probFeature[feature][int(state)] += 1
        #compute log-likelihood ratio
        for i in range(len(probFeature)):
            for j in range(len(probFeature[0])):
                probFeature[i][j] = probFeature[i][j] / float(sumc)
                probFeature[i][j] = probFeature[i][j] * probc / ((1-probFeature[i][j]) * (1-probc))
        return probFeature

    def reportBestK(self, k, probFeature):
        """
        Report the ten Si (feature number, variant and log-ratio) with the highest absolute
        log-likelihood ratios
        :param k: 10 here
        :param probFeature: matrix of log-likelihood ratio for each feature and state
        """
        bestK = []
        for ki in range(k):
            max = -1
            r = -1
            c = -1
            for row, i in enumerate(probFeature):
                for column, j in enumerate(i):
                    if j > max:
                        max = j
                        r = row
                        c = column
                        probFeature[row][column] = -1
            bestK.append([max, r, c])
            print("#" + str(ki+1) + ": " + str(max) + "(log ratio), " + str(r) + "(feature number), " + str(c) + "(state variant)")


m = Model()
m.readTSV("training1.tsv")
probc = m.classify()
probFeature = m.conditionalProb(probc)
m.reportBestK(10, probFeature)
