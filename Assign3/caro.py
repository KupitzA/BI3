import re
import math

class NaiveBayes:


    def __init__(self, filename_training):

        self.proportion = [0] * 2
        for i in range(2):
            self.proportion[i] = [0] * 401

        self.file = filename_training
        file_training = open(filename_training, "r")

        for line in file_training:

            sample = re.split(r'\t+', line)
            interaction = int(sample[0])
            self.proportion[interaction][0] = (self.proportion[interaction][0]) + 1

            for index, feature in enumerate(sample):
                if index != 0:
                    i = (index-1) * 4 + (int(feature)+1)
                    self.proportion[interaction][i] = self.proportion[interaction][i] + 1

    def predict_given_features(self, sample):

        total_interaction = float(self.proportion[1][0])
        total_no_interaction = float(self.proportion[0][0])
        total = total_interaction + total_no_interaction

        sum_p = 0.0
        for index, feature in enumerate(sample):
            if index != 0:

                i = (index-1) * 4 + (int(feature)+1)
                feature_interaction = float(self.proportion[1][i])
                feature_no_interaction = float(self.proportion[0][i])
                total = feature_interaction + feature_no_interaction
                if (total != 0) & (feature_no_interaction != 0) & (feature_interaction != 0):
                    sum_p = sum_p + math.log((feature_interaction / total_interaction) / (feature_no_interaction / total_no_interaction))


        return sum_p + math.log((total_interaction/total) / (total_no_interaction/total))


    def test(self, filename_test):

        file_test = open(filename_test, "r")

        result = []
        accuracy = 0.0
        total = 0
        for line in file_test:
            total = total + 1
            sample = re.split(r'\t+', line)
            classified = self.predict_given_features(sample)
            if ((classified > 0) & (int(sample[0])) == 1) | ((classified <= 0) & (int(sample[0]) == 0)):
                accuracy = accuracy + 1
                result.append([classified, "true"])

            else:
                result.append([classified, "false"])

        print(accuracy/total)
        return result


if __name__ == "__main__":
        bayes = NaiveBayes("training1.tsv")
        print(bayes.proportion[1])
        print(bayes.proportion[0])
        print(NaiveBayes.test(bayes, "test1.tsv"))