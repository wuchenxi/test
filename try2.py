from random import random
from statistics import *
from scipy.stats import *
import sys
data=open("sp500.csv")
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

start_month=int(sys.argv[1])
duration=int(sys.argv[2])

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

print(months[start_month][0])

results=[]
for d in range(1, 32):
    returns=0
    for k in range(start_month, start_month+duration):
        returns+=1/get_price(months[k], d)
    returns=returns*months[start_month+duration][0][1]/duration
    results+=[(d, returns)]

returns=0
for k in range(start_month, start_month+duration):
    prices=[0]*31
    for j in range(k-13, k-11):
        for d in range(31):
            prices[d]+=1/get_price(months[j], d+1)
    dmin=0
    for i in range(31):
        if prices[i]>prices[dmin]:
            dmin=i
    dmin+=1
    returns+=1/get_price(months[k], dmin)
returns=returns*months[start_month+duration][0][1]/duration
results+=[(0, returns)]
results.sort(key=lambda x: -x[1])
for l in results:
    print(l)
