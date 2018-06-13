from data_matrix import DataMatrix
from network import CorrelationNetwork
from correlation import CorrelationMatrix
from cluster import CorrelationClustering


def exercise_1():
    DM1 = DataMatrix('expression.tsv')
    DM1.to_tsv('Flohr_Kupitz_expression.tsv')
    print(DM1.not_normal_distributed(0.05, True))
    DM2 = DataMatrix('methylation.tsv')
    DM2.to_tsv('Flohr_Kupitz_methylation.tsv')
    print(DM2.not_normal_distributed(0.05, True))

def exercise_3():
    # TODO
    pass


def exercise_4():
    # TODO
    pass

# only execute the following if this module is the entry point of the program, not when it is imported into another file
if __name__ == '__main__':
    exercise_1()
    exercise_3()
    exercise_4()