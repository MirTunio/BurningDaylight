# Simulation of Cocktail Party phenomenon in Linked by Barabasi
# Modelling the connectivity threshold after which networks form large groups (communities/clusters/circles/Groups etc.)
# 


# Start with N nodes
# With random probability at each iteration, connect each node with one other
# Measure size of largest cluster
# ------------------

# Going to have N sets in the start, with each iteration union sets and measure size of largest
import numpy.random as r
import matplotlib.pyplot as plt
import numpy as np


N = 2000
Party = [{n} for n in xrange(N)]
Iterations = 2000
maxlog = []
avglog = []
alllog = []

for i in xrange(Iterations):
#    print('--------------')
#    print(i)

    if len(Party) == 1:
        break

    newParty = []

    Glen = len(Party)

    dice1 = r.randint(Glen)
    dice2 = r.randint(Glen)

    for i in range(Glen):
        if i != dice1 and i != dice2:
            newParty.append(Party[i])

    if dice1 != dice2:
        G1 = Party[dice1]
        G2 = Party[dice2]
        G = G1.union(G2)

        newParty.append(G)
    else:
        newParty.append(Party[dice1])

    Party = newParty
    newParty = []

    lens = map(len,Party)
    MAXlen = max(lens)
    AVGlen = np.average(lens) - 1

    alllog.append(lens)
    maxlog.append(MAXlen)
    avglog.append(AVGlen)

#    print(Party)
#    print(lens)

#%%
plt.plot(maxlog)
plt.xlabel('Iterations')
plt.ylabel('Max group size')
plt.show()

plt.plot(avglog)
plt.xlabel('Iterations')
plt.ylabel('Avg group size')
plt.show()

plt.scatter(avglog,maxlog)
plt.xlabel('Avg group size')
plt.ylabel('Max group size')
plt.show()

#%%
trueIter = len(alllog)
for i in range(trueIter):
    P = alllog[i]
    I = [i]*len(P)
    if np.average(P) >= 2:
        plt.scatter(I,P,alpha=0.5,c='r',linewidth=0.0)
    else:
        plt.scatter(I,P,alpha=0.5,c='blue',linewidth=0.0)

plt.ylabel('All group sizes')
plt.xlabel('Itertaions')
plt.show()



