'''
KELLY criterion
Assigning dollar values to the amount of risk you take

I want you to prove that the Kelly Criterion is useful
'''
from sympy import *
import pandas as pd
from matplotlib import pyplot as plt
from pylab import rcParams
import numpy as np
rcParams['figure.figsize'] = 16,11

#%% Proof

x,b,p = symbols('x b p')
y = p*log(1+b*x) + (1-p)*log(1-x)
print(solve(diff(y,x), x))
#[-(1 - p - b*p)/b]

#%% Scenario
'''
For each bet one stands to win 2$ or lose 1$

'''
Bankroll = 1000
Odds = 1.5 # 2:1
Pwin = 0.60
Plose = 1-Pwin
Time = 100

BankrollLogs = pd.DataFrame(columns=['Kelly','Naive','Expected'])
#%% Kelly
BankrollKelly = Bankroll

def Kelly(Bankroll,Odds,Pwin,Plose):
    f = (Odds*Pwin - Plose)/Odds
    KellyBet = f*Bankroll
    return KellyBet

#%% Naive
BankrollNaive = Bankroll

def Naive(Bankroll,Odds,Pwin,Plose):
    NaiveRate = 0.10
    NaiveBet = NaiveRate*Bankroll
    return NaiveBet

#%% Expected Returns

BankrollExpected = Bankroll

def Expected(Bankroll,Odds,Pwin,Plose):
    RiskAppetite = 600 #1 implies you bet it's expected worth
    ExpectedBet = RiskAppetite*Pwin*Odds #you bet the expected worth of the bet
    return ExpectedBet

#%% Trial

Outcomes = [1*Odds if x == 1 else -1 for x in [np.random.randint(2) for i in range(Time)]]

for outcome in Outcomes:
    BankrollLogs = BankrollLogs.append({'Kelly':BankrollKelly,'Naive':BankrollNaive,'Expected':BankrollExpected},ignore_index=True)
    ExpectedBet = Expected(BankrollExpected,Odds,Pwin,Plose)
    NaiveBet = Naive(BankrollNaive,Odds,Pwin,Plose)
    KellyBet = Kelly(BankrollKelly,Odds,Pwin,Plose)

    BankrollExpected += ExpectedBet*outcome
    BankrollKelly += KellyBet*outcome
    BankrollNaive += NaiveBet*outcome

#BankrollLogs['Outcomes'] = Outcomes
np.log(BankrollLogs).plot(grid=True)
plt.ylabel = 'Log Bankroll'
plt.xlabel = 'Time'
plt.show()
print(BankrollLogs.tail(1))










