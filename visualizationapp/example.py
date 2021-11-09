from scipy.stats import chi2_contingency
from scipy.stats import kruskal

from scipy.stats import chisquare

from scipy.stats import wilcoxon
import numpy


# table = [0,2,2,0,3]

# stat, p = wilcoxon([0,2,2,0,3],[0,2,2,0])
# print(stat)
# print(p)



# number 1
try:
    table_ABC1 = [[306,116,163,367],[122,54,143,29],[96,37,53,18]]
    stat, p, dof, expected = chi2_contingency(table_ABC1)
    abc1_pvalue = round(p,3)
except:
    abc1_pvalue = 0

print(abc1_pvalue)



