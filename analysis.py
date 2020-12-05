from datetime import datetime
from math import *
from statsmodels.tsa.stattools import *
from statsmodels.tsa.api import *
from statsmodels.tsa.arima import *
import numpy as np

data=open("sp500.csv")
next(data)
l=next(data)
ll=l.split(",")
pre=float(ll[4])
returns=[]
day_of_month=[]
day_in_week=[]
months=[]
for l in data:
    ll=l.split(",")
    ld=ll[0].split("-")
    dt=datetime(int(ld[0]), int(ld[1]), int(ld[2]))
    cur=float(ll[4])
    returns+=[log(cur/pre)]
    pre=cur
    day_in_week+=[dt.weekday()]
    day_of_month+=[int(ld[2])-1]
    months+=[int(ld[1])-1]
n=len(returns)
x=[]
for i in range(n):
    if day_of_month[i]<7.5:
        x+=[[1,0,0,0]]
    elif day_of_month[i]<15.5:
        x+=[[0,1,0,0]]
    elif day_of_month[i]<22.5:
        x+=[[0,0,1,0]]
    else:
        x+=[[0,0,0,1]]
X=np.array(x)
nt=n-1000
train=returns[:nt]
train_X=X[:nt]
test=returns[nt:]
test_X=X[nt:]
print(adfuller(returns))
print(kpss(returns, nlags="auto"))
model_es=ExponentialSmoothing(train, initialization_method="estimated").fit()
forecast_es=model_es.forecast(1000)
error=0
for i in range(1000):
    error+=(test[i]-forecast_es[i])**2

print(sqrt(error))

model_arima=ARIMA(train, #exog=train_X,
                  order=(2, 0, 2)).fit()
print(model_arima.summary())
print(model_arima.params)
forecast_arima=model_arima.predict(1000)#, exog=test_X)
error=0
for i in range(1000):
    error+=(test[i]-forecast_arima[i])**2
print(sqrt(error))
lp=model_arima.params[5:]
