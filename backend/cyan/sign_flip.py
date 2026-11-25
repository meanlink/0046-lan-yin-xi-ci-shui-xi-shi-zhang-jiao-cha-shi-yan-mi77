from itertools import product
from statistics import median

def estimate(gains):
    grid=[round(g*10000) for g in gains]
    observed=abs(sum(grid))
    extreme=sum(abs(sum(a*b for a,b in zip(grid,signs)))>=observed
                for signs in product((-1,1),repeat=len(grid)))
    return float(median(gains)),extreme/2**len(grid)
