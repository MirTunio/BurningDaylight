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
Time = 10000

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

topplers = set()

def topple(Sandbox,Time,Sand,Ydim=Ydim,Xdim=Xdim):
    t = 0
    Sandbox[len(Sandbox)/2 + Xdim/2] = Sand
    topplers.add(len(Sandbox)/2 + Xdim/2)
    
    while t < Time:
        if len(topplers) == 0:
            break
        
        for loc in topplers.copy():
            pile_height = Sandbox[loc]
            new_height = pile_height % 4
            Sandbox[loc] = new_height
            spill_height = (pile_height - new_height) / 4
            Sandbox[loc+1] += spill_height
            Sandbox[loc-1] += spill_height
            Sandbox[loc+Ydim] += spill_height
            Sandbox[loc-Ydim] += spill_height
            
            topplers.remove(loc)
            topplers.add(loc+1) if Sandbox[loc+1] > 3 else None
            topplers.add(loc-1) if Sandbox[loc-1] > 3 else None
            topplers.add(loc+Ydim) if Sandbox[loc+Ydim] > 3 else None
            topplers.add(loc-Ydim) if Sandbox[loc-Ydim] > 3 else None
                
        t+=1
    print(max(Sandbox))
    

#%% RUN
topple(Sandbox,Time,Sand)    
show(Sandbox)  
    
    
    
    
    
    
    