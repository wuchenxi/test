from random import random
from statistics import *
from scipy.stats import *
import sys
import numpy as np
import matplotlib.pyplot as plt

data=open("nasdaq.csv")
next(data)
months=[[]]
for l in data:
    ll=l.split(",")
    ld=ll[0].split("-")
    day=int(ld[2])
    price=float(ll[4])
    if len(months[-1])>0 and day<months[-1][-1][0]:
        months+=[[]]
    months[-1]+=[(day, price, ld[0], ld[1])]
months=months[1:-1]
n=len(months)


def get_price(m, d):
    if d<m[0][0]:
        return m[0][1]
    elif d>m[-1][0]:
        return m[-1][1]
    else:
        for day in m:
            if day[0]>=d:
                return day[1]
    return 0

invprices=[]
for month in months:
    prices=[1/get_price(month, d+1) for d in range(31)]
    invprices+=[prices]
X=np.array(invprices[-240:])
X=(X-np.min(X))/(np.max(X)-np.min(X))
plt.imshow(X, cmap='hot', interpolation='nearest')
plt.show()
