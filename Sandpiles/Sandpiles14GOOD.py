'''
Sandpiles (re-write)
https://en.wikipedia.org/wiki/Abelian_sandpile_model

Life thrives on the edge of chaos. 
Living between ordered and chaotic regimes, at a critical point. 

'This compromise between order and surprise - appears best able
to coordinate complex activities and best able to evolve as well'
- Stuart Kauffman

The sandpile model demonstrates how such critical points arise
in nature. The pile of sand is constantly on the verge of chaos
as each new grain is added. When these piles collaps we find 
beautiful patterns left behind.

These beautiful patterns are emergent properties of the sand-
pile model. They come about even if we topple each sand pile
in a random way. These patterns are symbolic of life. 
'''

import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 30,30

#%% SETUP
Xdim = 1500
Ydim = 1500
Sandbox = np.array([0 for i in range(Xdim*Ydim)]) #Note that this is a 1d array for optimization purposes, it is reshaped to display
Sand = 2**30 #How many grains of sand in the center of the grid we start out with
Time = 100000000000 #How many times do we topple?

#%% DISPLAY - displays a picture of the sandpile
def show(Sandbox,Sand = Sand):
    Sandbox2D = Sandbox.reshape(Xdim,Ydim) #Reshape the 1d array for display
    plt.matshow(Sandbox2D,cmap='plasma',vmin = 0, vmax = 3)
    plt.title('Zero for {0} grains'.format(Sand))
    plt.show()
    
#%% TOPPLE - This section topples the sand as many times as is specified in the Time variable
def topple(Sandbox,Time,Sand,Ydim=Ydim,Xdim=Xdim):
    t = 0
    Sandbox[len(Sandbox)/2 + Xdim/2] = Sand
    while t < Time: 
        #print(max(Sandbox))
        too_high = np.nonzero(Sandbox > 3) #Creates a list of all the piles of sand which are ripe to topple
        if len(too_high[0]) < 1: #Condition for when all grains of sand which could be toppled have been toppled
            break
        loc = too_high[0]
        pile_height = Sandbox[loc]
        new_height = pile_height % 4 #The actual toppling occurs after this line
        Sandbox[loc] = new_height
        spill_height = (pile_height - new_height) / 4
        Sandbox[loc+1] += spill_height
        Sandbox[loc-1] += spill_height
        Sandbox[loc+Ydim] += spill_height
        Sandbox[loc-Ydim] += spill_height
        t+=1
        if t%10000 == 0:
            print('time is {0}'.format(t))
    print(max(Sandbox))
    

#%% RUN
topple(Sandbox,Time,Sand)    
show(Sandbox)  
