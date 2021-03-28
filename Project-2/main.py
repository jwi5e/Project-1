''' This code was written and tested by Jamee Wise and Nicholas Gross.'''
#%%
import random
import simpy


SERVED = 0
SERVICE_TIME = 0
ORDER_WINDOWS = 1   # Number of order windows
SERVED_DATA = []    # Number of people served per run
TIME_DATA = []      # Average service time per run
SIM_NUM = 50

ARRIVAL_DATA = []
ORDER_DATA = []
PAYMENT_DATA = []
PICKUP_DATA = []

numBins = 30

class Car:

    carNumber = 0

    def __init__(self, env, res):
        self.env = env
        self.res = res
        Car.carNumber += 1
        self.name = Car.carNumber

    def drive(self):
        self.arrivalTime = self.env.now
        print('Arrival::', self)
        req = self.res[0].request()
        yield req

        order = self.res[1].request()
        yield order
        self.res[0].release(req)
        print('Start ordering::', self)
        self.orderTime = random.lognormvariate(54.505/60, 55.883/60)
        ORDER_DATA.append(self.orderTime)
        evt = self.env.timeout(self.orderTime)
        yield evt
        print("Finish ordering::", self)
        self.foodPrepTime = random.weibullvariate(3, 2.0)
        foodPrep = self.env.timeout(self.foodPrepTime)


        req2 = self.res[2].request()
        yield req2
        self.res[1].release(order)


        req3 = self.res[3].request()
        yield req3
        self.res[2].release(req2)
        print('Start paying::', self)
        self.payTime = random.lognormvariate(58.661/60, 57.834/60)
        PAYMENT_DATA.append(self.payTime)
        pay = self.env.timeout(self.payTime)
        yield pay
        print("Finish paying::", self)


        req4 = self.res[4].request()
        yield req4
        self.res[3].release(req3)
        print('Waiting for pickup::', self)


        req5 = self.res[5].request()
        yield req5
        self.res[4].release(req4)
        print('Start pickup::', self)
        self.pickupTime = random.lognormvariate(58.661/60, 57.834/60)
        PICKUP_DATA.append(self.pickupTime)
        pickup = self.env.timeout(self.pickupTime)
        val = yield pickup & foodPrep # simpy.anyOf(evt,evt,evt)

        print("Finish pickup::", self)
        
        if pickup in val:
            print('food was ready waited to pay')
        elif foodPrep in val:
            print("food wasn't ready had to wait")
        else:
            print("oops")
        
        global SERVED
        SERVED += 1
        
        endTime = self.env.now
        global SERVICE_TIME
        SERVICE_TIME += endTime - self.arrivalTime
        
        self.res[5].release(req5)

    def __str__(self):
        return f'Car: {self.name:d} time: {self.env.now:.3f}'

def arrivalGen(env, res):

    while True:

        c = Car(env, res)
        env.process(c.drive())
        ar = random.weibullvariate(0.877, 58.541/60)
        ARRIVAL_DATA.append(ar);
        evt = env.timeout(ar)
        yield evt


for i in range(SIM_NUM):  
    env = simpy.Environment()
    
    initialLine = simpy.Resource(env, 7)
    orderWindow = simpy.Resource(env, ORDER_WINDOWS)
    betweenOrderAndPay = simpy.Resource(env, 4)
    payWindow = simpy.Resource(env,1)
    betweenPayAndPickup = simpy.Resource(env, 1)
    pickupWindow = simpy.Resource(env,1)
    
    res = [initialLine, orderWindow, betweenOrderAndPay, payWindow, betweenPayAndPickup, pickupWindow]
    
    env.process(arrivalGen(env, res))
    
    env.run(until=20.0)

SERVED_DATA.append(SERVED/1)
TIME_DATA.append(SERVICE_TIME/SERVED)
SERVED = 0
SERVICE_TIME = 0

# print('\nARRIVAL_DATA::', ARRIVAL_DATA)
# print('\nORDER_DATA::', ORDER_DATA)
# print('\nPAYMENT_DATA::', PAYMENT_DATA)
# print('\nPICKUP_DATA::', PICKUP_DATA)

#%%
# THIS IS FOR ARRIVAL_DATA

import matplotlib.pyplot as plt
from scipy import stats

#describe calculates statistics
sampleSize, min_max, sampleMean, sampleVariance, skew, kurtosis= stats.describe(ARRIVAL_DATA)
print(f'mean {sampleMean:0.3f}  variance: {sampleVariance:0.3f} range: ({min_max[0]:f}, {min_max[1]:f})')

std = stats.tstd(ARRIVAL_DATA)
print(f'standard deviation {std:0.3f}')

#generating plots of data
#have every bin to have at least 5 points
binSize = [5, 10, 20, 50, 100]
fig, axs = plt.subplots(len(binSize), 1)
plt.subplots_adjust(hspace=.5)

titleLabel = 'Arrival Data Histogram'
                                 
fig.suptitle(titleLabel)
for idx, ax in enumerate(axs):
    ax.hist(ARRIVAL_DATA, bins=binSize[idx])

plt.show()

#%%
# THIS IS FOR ORDER_DATA

import matplotlib.pyplot as plt
from scipy import stats

#describe calculates statistics
sampleSize, min_max, sampleMean, sampleVariance, skew, kurtosis= stats.describe(ORDER_DATA)
print(f'mean {sampleMean:0.3f}  variance: {sampleVariance:0.3f} range: ({min_max[0]:f}, {min_max[1]:f})')

std = stats.tstd(ORDER_DATA)
print(f'standard deviation {std:0.3f}')

#generating plots of data
#have every bin to have at least 5 points
binSize = [5, 10, 20, 50, 100]
fig, axs = plt.subplots(len(binSize), 1)
plt.subplots_adjust(hspace=.5)

titleLabel = 'Order Data Histogram'
                                 
fig.suptitle(titleLabel)
for idx, ax in enumerate(axs):
    ax.hist(ORDER_DATA, bins=binSize[idx])

plt.show()

#%%
# THIS IS FOR PAYMENT_DATA

import matplotlib.pyplot as plt
from scipy import stats

#describe calculates statistics
sampleSize, min_max, sampleMean, sampleVariance, skew, kurtosis= stats.describe(PAYMENT_DATA)
print(f'mean {sampleMean:0.3f}  variance: {sampleVariance:0.3f} range: ({min_max[0]:f}, {min_max[1]:f})')

std = stats.tstd(PAYMENT_DATA)
print(f'standard deviation {std:0.3f}')

#generating plots of data
#have every bin to have at least 5 points
binSize = [5, 10, 20, 50, 100]
fig, axs = plt.subplots(len(binSize), 1)
plt.subplots_adjust(hspace=.5)

titleLabel = 'Payment Data Histogram'
                                 
fig.suptitle(titleLabel)
for idx, ax in enumerate(axs):
    ax.hist(PAYMENT_DATA, bins=binSize[idx])

plt.show()

#%%
# THIS IS FOR PICKUP_DATA

import matplotlib.pyplot as plt
from scipy import stats

#describe calculates statistics
sampleSize, min_max, sampleMean, sampleVariance, skew, kurtosis= stats.describe(PICKUP_DATA)
print(f'mean {sampleMean:0.3f}  variance: {sampleVariance:0.3f} range: ({min_max[0]:f}, {min_max[1]:f})')

std = stats.tstd(PICKUP_DATA)
print(f'standard deviation {std:0.3f}')

#generating plots of data
#have every bin to have at least 5 points
binSize = [5, 10, 20, 50, 100]
fig, axs = plt.subplots(len(binSize), 1)
plt.subplots_adjust(hspace=.5)

titleLabel = 'Pickup Data Histogram'
                                 
fig.suptitle(titleLabel)
for idx, ax in enumerate(axs):
    ax.hist(PICKUP_DATA, bins=binSize[idx])

plt.show()

#%%
# check chi square goodness of fit of a weibull distribution  ARRIVAL_DATA

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# observed
binEdges = np.linspace(0.0, np.max(ARRIVAL_DATA), numBins)
observed, _ = np.histogram(ARRIVAL_DATA, bins=binEdges)


# MLE 
fit_alpha, fit_loc, fit_beta=stats.weibull_min.fit(ARRIVAL_DATA, floc=0)
print(f'fit_alpha {fit_alpha:0.3f} fit_beta {fit_beta:0.3f}')

# expected
expectedProb = stats.weibull_min.cdf(binEdges, fit_alpha, scale=fit_beta, loc=fit_loc)
expectedProb[-1] += 1.0 - np.sum(np.diff(expectedProb))
expected = sampleSize * np.diff(expectedProb)

binMidPt = (binEdges[1:] + binEdges[:-1]) / 2
plt.hist(ARRIVAL_DATA, bins=binEdges, label='Observed')
plt.plot(binMidPt, expected, 'or-', label='Expected')
plt.plot(binMidPt, observed, 'oy-', label='Observed')
plt.legend()

chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected, ddof=0)
print(f'ChiSquare Statistic {chiSq:0.3f} P value {pValue:0.3f}')

print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')

if pValue >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')
    
#%%
# check chi square goodness of fit of a lognormal distribution ORDER_DATA

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# observed
binEdges = np.linspace(0.0, np.max(ORDER_DATA), numBins)
observed, _ = np.histogram(ORDER_DATA, bins=binEdges)

# MLE 
fit_alpha, fit_loc, fit_beta=stats.lognorm.fit(ORDER_DATA, floc=0)
print(f'fit_alpha {fit_alpha:0.3f} fit_beta {fit_beta:0.3f}')

# expected
expectedProb = stats.lognorm.cdf(binEdges, fit_alpha, scale=fit_beta, loc=fit_loc)
expectedProb[-1] += 1.0 - np.sum(np.diff(expectedProb))
expected = sampleSize * np.diff(expectedProb)

binMidPt = (binEdges[1:] + binEdges[:-1]) / 2
plt.hist(ORDER_DATA, bins=binEdges, label='Observed')
plt.plot(binMidPt, expected, 'or-', label='Expected')
plt.plot(binMidPt, observed, 'oy-', label='Observed')
plt.legend()

chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected)
print(f'ChiSquare Statistic {chiSq:0.3f} P value {pValue:0.3f}')

print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')

if pValue >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')
    
#%%
# check chi square goodness of fit of a lognormal distribution  PAYMENT_DATA

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# observed
binEdges = np.linspace(0.0, np.max(PAYMENT_DATA), numBins)
observed, _ = np.histogram(PAYMENT_DATA, bins=binEdges)

# MLE 
fit_alpha, fit_loc, fit_beta=stats.lognorm.fit(PAYMENT_DATA, floc=0)
print(f'fit_alpha {fit_alpha:0.3f} fit_beta {fit_beta:0.3f}')

# expected
expectedProb = stats.lognorm.cdf(binEdges, fit_alpha, scale=fit_beta, loc=fit_loc)
expectedProb[-1] += 1.0 - np.sum(np.diff(expectedProb))
expected = sampleSize * np.diff(expectedProb)

binMidPt = (binEdges[1:] + binEdges[:-1]) / 2
plt.hist(PAYMENT_DATA, bins=binEdges, label='Observed')
plt.plot(binMidPt, expected, 'or-', label='Expected')
plt.plot(binMidPt, observed, 'oy-', label='Observed')
plt.legend()

chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected)
print(f'ChiSquare Statistic {chiSq:0.3f} P value {pValue:0.3f}')

print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')

if pValue >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')
    
#%%
# check chi square goodness of fit of a lognormal distribution PICKUP_DATA

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# observed
binEdges = np.linspace(0.0, np.max(PICKUP_DATA), numBins)
observed, _ = np.histogram(PICKUP_DATA, bins=binEdges)

# MLE 
fit_alpha, fit_loc, fit_beta=stats.lognorm.fit(PICKUP_DATA, floc=0)
print(f'fit_alpha {fit_alpha:0.3f} fit_beta {fit_beta:0.3f}')

# expected
expectedProb = stats.lognorm.cdf(binEdges, fit_alpha, scale=fit_beta, loc=fit_loc)
expectedProb[-1] += 1.0 - np.sum(np.diff(expectedProb))
expected = sampleSize * np.diff(expectedProb)

binMidPt = (binEdges[1:] + binEdges[:-1]) / 2
plt.hist(PICKUP_DATA, bins=binEdges, label='Observed')
plt.plot(binMidPt, expected, 'or-', label='Expected')
plt.plot(binMidPt, observed, 'oy-', label='Observed')
plt.legend()

chiSq, pValue = stats.chisquare(f_obs=observed, f_exp=expected)
print(f'ChiSquare Statistic {chiSq:0.3f} P value {pValue:0.3f}')

print('H0: (null hypothesis) Sample data follows the hypothesized distribution.')
print('H1: (alternative hypothesis) Sample data does not follow a hypothesized distribution.')

if pValue >= 0.05:
    print('we can not reject the null hypothesis')
else:
    print('we reject the null hypothesis')
    
