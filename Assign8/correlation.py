from itertools import combinations
from copy import copy

def computeIndex(vec):
	"""
	Compute the idices for a subsequenc of equal values
	"""
	temp = 0
	for i in vec:
		temp += i
	return float(temp)/float(len(vec))
	
def initializeIndices(x_s):
	"""
	Create list of indices for values, where equal values
	in x_s get equal averaged idices
	"""
	x_r = list(range(0, len(x_s)))
	# add an terminate-sign to end the algorithm
	x_r.append(-1)
	i = 0
	for j in range(1, len(x_s)):
		if x_s[i] != x_s[j]:
			index = computeIndex(x_r[i:j])
			while i < j:
				x_r[i] = index
				i += 1
	# return all but the last termination-sign
	return x_r[0:len(x_s)]

def bubble(x_s):
	"""
	Recursive bubble sorting with "rebubbling"
	the indices with resprect to multi-occurring
	values
	"""
	for i in range(1,len(x_s)):
		if x_s[i-1] < x_s[i]:
			# swap list elements
			temp = x_s[i-1]
			x_s[i-1] = x_s[i]
			x_s[i] = temp
			# next bubble
			x_r = bubble(x_s)
			# reverse bubbleing of the indices
			temp = x_r[i-1]
			x_r[i-1] = x_r[i]
			x_r[i] = temp
			return x_r
	# called only in the deepest recursive step
	# here the indices get initialized
	return initializeIndices(x_s)
			
def rank(x):
    """
    :param x: a list of values
    :return: ranking of the input list
    """
    # sort the values of x by bubble sort
    # original indices are kept in a second list
    return bubble(copy(x))

def pearson_correlation(x, y):
    """
    :param x: a list of values
    :param y: a list of values
    :return: Pearson correlation coefficient of X and Y
    """
    # TODO

def spearman_correlation(x, y):
    """
    :param x: a list of values
    :param y: a list of values
    :return: Spearman correlation coefficient of X and Y
    """
    # TODO


def kendall_correlation(x, y):
    """
    :param x: a list of values
    :param y: a list of values
    :return: Kendall-B correlation coefficient of X and Y
    """
    # TODO


class CorrelationMatrix(dict):
    """
    This class behaves like a dictionary, where the correlation between two elements 1 and 2 is accessible via
    cor_matrix[(element_1, element_2)] or cor_matrix[(element_2, element_1)] since the matrix is symmetrical.
    It also stores the row (or column) names of the input DataMatrix.
    """
    def __init__(self, data_matrix, method, rows):
        """
        :param data_matrix: a DataMatrix (see data_matrix.py)
        :param method: string specifying the correlation method, must be 'Pearson', 'Spearman' or 'Kendall'
        :param rows: True if the correlation matrix should be constructed for the rows, False if for the columns
        """
        # initialise the dictionary
        super().__init__(self)

        # if rows = True, then compute the correlation matrix for the row data
        if rows:
            data = data_matrix.get_rows()
        # if rows = False, then compute the correlation matrix for the column data
        else:
            data = data_matrix.get_columns()

        # sorted list of row names (or column names) in the input data matrix
        self.names = list(sorted(data.keys()))

        # compute the correlation between all pairs of rows (or columns)
        for name_1, name_2 in combinations(data.keys(), 2):
            # use the specified correlation method
            if method == 'Pearson':
                correlation = pearson_correlation(data[name_1], data[name_2])
            elif method == 'Spearman':
                correlation = spearman_correlation(data[name_1], data[name_2])
            elif method == 'Kendall':
                correlation = kendall_correlation(data[name_1], data[name_2])
            else:
                raise ValueError('The correlation method not supported must be either Pearson, Spearman or Kendall.')

            # add the correlation symmetrically
            self[(name_1, name_2)] = correlation
            self[(name_2, name_1)] = correlation
