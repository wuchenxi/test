from random import random
from statistics import *
from scipy.stats import *
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
returns_list=[[] for i in range(31)]
print(months[100][0])
for start in range(100, 112):
    for d in range(1, 32):
        returns=0
        curprice=0
        for k in range(start, start+120):
            if d<months[k][0][0]:
                returns+=1/months[k][0][1]
                curprice=months[k][0][1]
            elif d>months[k][-1][0]:
                returns+=1/months[k][-1][1]
                curprice=months[k][-1][1]
            else:
                for day in months[k]:
                    if day[0]>=d:
                        returns+=1/day[1]
                        curprice=day[1]
                        break
        returns_list[d-1]+=[returns*curprice/120]
print(friedmanchisquare(*returns_list))
lst=[]
for i in range(31):
    lst+=[(i+1, median(returns_list[i]))]
lst.sort(key=lambda x:-x[1])
for l in lst:
    print(l)
