import csv
import numpy
import math
from scipy import stats

class DataMatrix:
    def __init__(self, file_path):
        """
        :param file_path: path to the input matrix file
        """
        self.file_path = file_path
        # TODO: define and initialise the class fields you need for your implementation
        # read the matrix in the input file, remove rows with empty values and merge duplicate rows
        self.cols, self.rows = self.read_data()

    def read_data(self):
        """
        Reads data from a given matrix file, where the first line gives the names of the columns and the first column
        gives the names of the rows. Removes rows with empty or non-numerical values and merges rows with the same
        name into one.
        """
        with open(self.file_path) as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            cols = next(reader)
            fields = len(cols)
            rows = dict()
            for row in reader:
                if len(row) == fields:
                    floats = []
                    nan = False
                    for i in range(1, fields):
                        try:
                            f = float(row[i])
                            if math.isnan(f):
                                nan = True
                        except ValueError:
                            nan = True
                        floats.append(f)
                    if row[0] not in rows and not nan:
                        rows[row[0]] = [floats]
                    elif not nan:
                        rows[row[0]].append(floats)
            for k, v in rows.items():
                if len(v) > 1:
                    value = []
                    for i in range(0, len(v[0])):
                        mean = []
                        for j in range(0, len(v)):
                            mean.append(v[j][i])
                        value.append(numpy.mean(mean))
                    rows[k] = [value]
        return cols, rows

    def get_rows(self):
        """
        :return: dictionary with keys = row names, values = list of row values
        """
        rows = dict()
        for k, v in self.rows.items():
            rows[k] = v[0]
        return self.rows

    def get_columns(self):
        """
        :return: dictionary with keys = column names, values = list of column values
        """
        dic = dict()
        for k, v in self.rows.items():
            for i, col in enumerate(self.cols):
                if i != 0:
                    if col not in dic:
                        dic[col] = []
                    else:
                        dic[col].append(v[0][i-1])
        return dic

    def not_normal_distributed(self, alpha, rows):
        """
        Uses the Shapiro-Wilk test to compute all rows (or columns) that are not normally distributed.
        :param alpha: significance threshold
        :param rows: True if the Shapiro-Wilk p-values should be computed for the rows, False if for the columns
        :return: dictionary with keys = row/columns names, values = Shapiro-Wilk p-value
        """
        dic = dict()
        values = self.get_rows() if rows else self.get_columns()
        for k, v in values.items():
            W, p = stats.shapiro(v)
            if p < alpha:
                dic[k] = p
        return dic

    def to_tsv(self, file_path):
        """
        Writes the processed matrix into a tab-separated file, with the same column order as the input matrix and
        the rows in lexicographical order.
        :param file_path: path to the output file
        """
        with open(file_path, 'w') as f:
            values = [value for (key, value) in sorted(self.get_rows().items())]
            keys = sorted(self.get_rows().keys())
            for i in range(0, len(values)):
                s = ''
                s += keys[i] + '\t'
                for j in values[i][0]:
                    s += str(j) + '\t'
                s += '\n'
                f.write(s)
