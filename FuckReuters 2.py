#Fuck Reuters
#Fuck Reuters harder - map the algorithm - optimize for statistics
#400 lines, 1 minute data

#Setup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 14,5

min1 = pd.read_csv('^VIX-equity-1-minute-20160210.csv')
#min1
#930AM to 415PM
#NOT 0 INDEXED
open1 = min1['open'][1:]
close1 = min1['close'][1:]
high1 = min1['high'][1:]
low1 = min1['low'][1:]

plt.plot(open1)
plt.plot(close1)
plt.plot(high1)
plt.plot(low1)
plt.ylim(22,28)
plt.xlim(0,405) #1more
plt.ylabel('$')
plt.xlabel('minute')
plt.legend(loc = 4)
plt.show()

pocket = 100
pocketlog = np.array([])

pocket2 = 100
pocketlog2 = np.array([])

def day(alg1,alg2):
    global pocket,pocketlog,pocket2,pocketlog2
    for i in np.arange(5,len(close1)):
        alg1(i)
        alg2(i)
        pocketlog = np.append(pocketlog,pocket)
        pocketlog2 = np.append(pocketlog2,pocket2)
        plt.plot(pocketlog,c='blue')
        plt.plot(pocketlog2,c='gold')
        plt.xlim(0,405) #1more
        plt.ylabel('$')
        plt.xlabel('minute')
        plt.legend(loc=4)
        plt.show()

#naive runs:

#assumptions: inertia

def basicrunavg(t):
    global pocket
    sample = close1[t-5:t]
    savg = np.average(sample)
    #print(savg)
    #print(t)
    if savg>close1[t]:
        print('buy')
        pocket -= close1[t]
    else:
        print("\x1b[31msel\x1b[0m")
        pocket += close1[t]
    print(pocket)

def marker5min(t):
    global pocket2
    marker = close1[t-4]
    #print(savg)
    #print(t)
    if marker>close1[t]:
        print('buy')
        pocket2 -= close1[t]
    else:
        print("\x1b[31msel\x1b[0m")
        pocket2 += close1[t]
    print(pocket)
    
def stochastic(t):
    global pocket2
    marker = np.random.rand()
    
    if marker>0.5:
        print('buy')
        pocket2 -= close1[t]
    else:
        print("\x1b[31msel\x1b[0m")
        pocket2 += close1[t]
    print(pocket2)
    
def basicstoch(t): #THIS IS FLAWED
    global pocket2
    sample = close1[t-5:t]
    impulse = np.random.rand() #random move, once in a while
    
    savg = np.average(sample)
    #print(savg)
    #print(t)
    if savg>close1[t] and impulse>0.5:
        print('buy')
        pocket2 -= close1[t]
    else:
        print("\x1b[31msel\x1b[0m")
        pocket2 += close1[t]
    print(pocket2)

    
    
day(basicrunavg,basicstoch)


##NOTES#########################
#
#So random seems to do better than 5marker
#So 5min avg seems to do better than random
#
#
#
#
#
#
#
#