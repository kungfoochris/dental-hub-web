from scipy.stats import chi2_contingency
from scipy.stats import kruskal

from scipy.stats import chisquare

from scipy.stats import wilcoxon
import numpy


table = [0,2,2,0,3]

# stat, p = wilcoxon(24,55)
# print(stat)
# print(p)


# from numpy.random import seed
# from numpy.random import randn
# from scipy.stats import wilcoxon
# # seed the random number generator

# list1 = [2,3,5]
# list1.insert(2, " ")
# print(list1)

# print("q"+list1[2])


# carries_risk_low_pvalue = chisquare([0.5,0.89])
# print(carries_risk_low_pvalue)
# a = round(carries_risk_low_pvalue[1],2)
# print(a)



try:
    table_ABC1 = [[0,1,0],[1,0,0],[0,0,0]]
    stat, p, dof, expected = chi2_contingency(table_ABC1)
    abc1_pvalue = round(p,3)
except:
    abc1_pvalue = 0


# print(type(repr(p)))
# print(p)
print(abc1_pvalue)

