import correlation

x = [2,  4,  1,  9,  9,  7,  0, 12]
#x = [6,6,4,2,10]
y = [3,  1, 20, 11,  1,  2,  5,  3]

x_r = correlation.rank(x)
print(x)
print(x_r)
print(correlation.pearson_correlation(x,y))
print(correlation.spearman_correlation(x,y))
