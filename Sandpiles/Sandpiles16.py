'''
Sandpiles (re-write)
https://en.wikipedia.org/wiki/Abelian_sandpile_model

Take to 1d array and lose the 'topple' function. LETS GET EFFIECIENT
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 10,10

#%% SETUP
Xdim = 1000
Ydim = 1000
Sandbox = np.array([0 for i in range(Xdim*Ydim)])
Sand = 2**20
Time = 1000

#%% DISPLAY
def show(Sandbox,Sand = Sand):
    Sandbox2D = Sandbox.reshape(Xdim,Ydim)
    plt.matshow(Sandbox2D,cmap='hot',vmin = 0, vmax = 3)
    plt.title('Zero for {0} grains'.format(Sand))
    plt.show()
    

#%% TOPPLE
'''
Attempt to get rid of the need to search the whole matrix each iteratiion
'''

def topple(Sandbox,Time,Sand,Ydim=Ydim,Xdim=Xdim):
    t = 0
    topplers = []
    Sandbox[len(Sandbox)/2 + Xdim/2] = Sand
    topplers += [(len(Sandbox)/2 + Xdim/2)]
    
    while t < Time:
        if len(topplers) == 0:
            break
        
        for i in xrange(len(topplers)):
            loc = topplers[i]
            pile_height = Sandbox[loc]
            new_height = pile_height % 4
            Sandbox[loc] = new_height
            spill_height = (pile_height - new_height) / 4
            Sandbox[loc+1] += spill_height
            Sandbox[loc-1] += spill_height
            Sandbox[loc+Ydim] += spill_height
            Sandbox[loc-Ydim] += spill_height
            
            del topplers[i]
            topplers.append(loc+1) if Sandbox[loc+1] > 3 else None
            topplers.append(loc-1) if Sandbox[loc-1] > 3 else None
            topplers.append(loc+Ydim) if Sandbox[loc+Ydim] > 3 else None
            topplers.append(loc-Ydim) if Sandbox[loc-Ydim] > 3 else None
                
        t+=1
    print(max(Sandbox))
    

#%% RUN
topple(Sandbox,Time,Sand)    
show(Sandbox)  
    
    
    
    