import csv
import math
import sys


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
                for i in range(1, 101):
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
        countnotc = len(self.classifier)-sumc
        probFeature = [0]*100
        probnotc = [0]*100
        for i in range(100):
            probFeature[i] = [0]*4
            probnotc[i] = [0]*4
        #probnotc = probFeature.copy()
        #count successfull classifications for each feature and state
        for rownumber, rowvalue in enumerate(self.featureMatrix):
            for feature, state in enumerate(rowvalue):
                if self.classifier[rownumber] == "1":
                    probFeature[feature][int(state)] += 1
                else:
                    probnotc[feature][int(state)] += 1
        #compute log-likelihood ratio
        for i in range(len(probFeature)):
            for j in range(len(probFeature[0])):
                if probnotc[i][j] != 0 and probFeature[i][j] != 0:
                    probFeature[i][j] = probFeature[i][j] / float(sumc) / (probnotc[i][j] / float(countnotc))
                    probFeature[i][j] = math.log(probFeature[i][j])
        return probFeature, probc

    def reportBestK(self, k, probFeature):
        """
        Report the ten Si (feature number, variant and log-ratio) with the highest absolute
        log-likelihood ratios
        :param k: 10 here
        :param probFeature: matrix of log-likelihood ratio for each feature and state
        """
        bestK = []
        print("enumeration of best features & log ratio & feature number & state variant\\")
        for ki in range(k):
            max = 0
            r = -1
            c = -1
            for row, i in enumerate(probFeature):
                for column, j in enumerate(i):
                    if math.fabs(j) > math.fabs(max):
                        max = j
                        r = row
                        c = column
                        probFeature[row][column] = sys.float_info.min
            bestK.append([max, r, c])
            print(str(ki+1) + " & " + str(max) + " & " + str(r) + " & " + str(c) + "\\")

    def prediction(self, probFeature, featureMatrix, probc):
        """
        Predicts the ability to interact for the protein pairs
        :param probFeature: matrix of log-likelihood ratio for each feature and state that was
        learned from trainings test set
        :param featureMatrix: Matrix with values of each feature from test file
        :param probc: probability to classify a protein pair to 1
        :return: list with classified interactions for each protein pair
        """
        classification = []
        for rowvalue in featureMatrix:
            probC = 0
            for feature, state in enumerate(rowvalue):
                probC += probFeature[feature][int(state)]
            probC += math.log(float(probc)/(1-probc))
            print(probC)
            c = 1 if probC > 0 else 0
            classification.append(c)
        print(classification)
        return classification

    def accuracy(self, classification):
        """
        Computes the accuracy of the classifier
        :param classification: list with classified interactions for each protein pair
        :return: accuracy of classification
        """
        accuracy = 0.0
        for i, c in enumerate(classification):
            if str(c) == self.classifier[i]:
                accuracy += 1
        accuracy = accuracy / (len(classification)-1)
        print(accuracy)


m = Model()
m.readTSV("training1.tsv")
probc = m.classify()
probFeature, probc = m.conditionalProb(probc)
m.reportBestK(10, probFeature)
mtest = Model()
mtest.readTSV("test1.tsv")
classification = m.prediction(probFeature, mtest.featureMatrix, probc)
m.accuracy(classification)
