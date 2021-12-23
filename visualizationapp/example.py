from scipy.stats import chi2_contingency
from scipy.stats import kruskal

from scipy.stats import chisquare

from scipy.stats import wilcoxon
import numpy


# table = [0,2,2,0,3]

stat, p = wilcoxon([0,0,0,0,0],[0,0,0,0,0])
print(stat)
print(p)



# number 1
# try:
#     table_ABC1 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
#     stat, p, dof, expected = chi2_contingency(table_ABC1)
#     print(p)
#     print(type(p))
#     if numpy.isnan(p):
#         abc1_pvalue = "nan" 
#     else:
#         abc1_pvalue = round(p,3)
#     print("inside try")
# except:
#     print("inside except")
#     abc1_pvalue = 0

# print(abc1_pvalue)


