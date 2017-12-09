'''
6 Degrees of Seperation
:: Monday Night Musings
GOOD EXERCISE
'''
from sympy import *
import pandas as pd
from matplotlib import pyplot as plt
from pylab import rcParams
import numpy as np
rcParams['figure.figsize'] = 10,10
import networkx as nx

#%% First Order - If there are really only 6 degrees of seperation
Population = 7000000000
Friends = 44
Degrees = 6

print('Population: ' +str(Population), 'Estimate: ' + str(44**6))

'''
Demonstrates that if an indivudal is really 6 degrees seperated
from any other individual, the average person must have 44
unique friends on average. (Unique wrt to any friendship)

For this to be the case, the individuals must more than 44 friends, proof:
    (avg. unique friends)^6 = 7BN
    avg. unique friends = log(7*(10**9))/log(44)
                         = 5.9904968246872441

So the question arises, how many friends must each individual have,
so that on average, each individual has 44 unique friends.
    ^^^ THIS will demonstrate to first order, the validity
    of the 6DOS argument by putting an average number to
    number of friends each individual has

    Need to show that on average those who share only one friend
    each have 44 other unique friends
'''

#%% Simulation 1 Random
'''
Creating a random network with 7B nodes, and attempting to obtain
the average seperation between nodes
A quick calculation shows the answer should be (ASASD)
'''
'''
Create a randomly connected graph, meausre the average length of path between all nodoes
Increase number of nodess iteratively and plot this average
Fit and extrapolate (should be power or factorial prog.)
'''

N = 500
Nodes = {}

DegreeList = []
NList = range(10,N,5)

for N in NList:
#    print(N)
    population = nx.gnp_random_graph(N, 0.5, seed=None, directed=False)

#   nx.drawing.nx_pylab.draw(population)
#    plt.show()

    shortest = nx.average_shortest_path_length(population)
#    print('Average: '+ str(shortest))
    DegreeList.append(shortest)

plt.plot(DegreeList, linewidth = 2, color = 'blue', alpha = 0.8)
plt.title('10 to 500 Nodes - Average Shortest Path - Randomly Connected')
plt.show()

#%% Simulation 2 Stogratz
'''
Same model as above except the number of connections is found by
Using a stogratz small world graph
'''


N = 500
Nodes = {}

DegreeList = []
NList = range(10,N,5)

for N in NList:
    population = nx.watts_strogatz_graph(N, 9 , p = 0.3)
#    nx.drawing.nx_pylab.draw(population)
#    plt.show()

    shortest = nx.average_shortest_path_length(population)
#    print('Average: '+ str(shortest))
    DegreeList.append(shortest)

plt.plot(DegreeList, linewidth = 2, color = 'blue', alpha = 0.8)
plt.title('10 to 500 Nodes - Average Shortest Path - Watts Stogratz Model')
plt.show()

#%% Simulation 3 Power Law
N = 500
Nodes = {}

DegreeList = []
NList = range(10,N,5)

for N in NList:
    population = nx.powerlaw_cluster_graph(N, 9 , p = 0.5)
#    nx.drawing.nx_pylab.draw(population)
#    plt.show()

    shortest = nx.average_shortest_path_length(population)
#    print('Average: '+ str(shortest))
    DegreeList.append(shortest)

plt.plot(DegreeList, linewidth = 2, color = 'blue', alpha = 0.8)
plt.title('10 to 500 Nodes - Average Shortest Path - PowerLaw Cluster Graph (Holme and Kim)')
plt.show()

#%% Simulation 4 Barabasi Albert
N = 500
Nodes = {}

DegreeList = []
NList = range(50,N,10)

for N in NList:
#    print(N)
#    population = nx.gnp_random_graph(N, 0.5, seed=None, directed=False)
    population = nx.barabasi_albert_graph(N,10)
#    nx.drawing.nx_pylab.draw(population)
#    plt.show()

    shortest = nx.average_shortest_path_length(population)
#    print('Average: '+ str(shortest))
    DegreeList.append(shortest)

plt.plot(DegreeList, linewidth = 2, color = 'blue', alpha = 0.8, marker = 'x')
plt.title('10 to 500 Nodes - Average Shortest Path - Barabasi-Albert Graph')
plt.xlable('Nodes')
plt.ylabel('Average Shortest Path')
plt.show()

#%%
from scipy.optimize import curve_fit

def BAvals(friends):
    N = 600
    Nodes = {}

    DegreeList = []
    NList = range(100,N,10)

    for N in NList:
        population = nx.barabasi_albert_graph(N,friends)
        shortest = nx.average_shortest_path_length(population)
        DegreeList.append(shortest)

    return DegreeList,NList

def logarithmic(x, a, b):
    return a*np.log(x) + b

at7BLog = []
params = []
fren = range(20,100,5)

for friends in fren:
    print(friends)
    Y,X = BAvals(friends)
    popt, pcov = curve_fit(logarithmic, X, Y)

    at7BLog.append(logarithmic(7000000000, *popt))
    params.append([popt])


plt.plot(fren,at7BLog)
plt.ylabel('DOS')
plt.xlabel('friends')
plt.grid()
plt.show()

