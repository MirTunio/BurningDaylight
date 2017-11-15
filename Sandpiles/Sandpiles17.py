'''
Sandpiles (re-write)
https://en.wikipedia.org/wiki/Abelian_sandpile_model

Take to 1d array and lose the 'topple' function. LETS GET EFFIECIENT
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 20,20

#%% SETUP
Xdim = 1000
Ydim = 1000
Sandbox = np.array([0 for i in range(Xdim*Ydim)])
Sand = 4*2**20
Time = 100000
upper = Xdim*Ydim-1
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
    #Sandbox[len(Sandbox)/2 + Xdim/2] = Sand
    Sandbox[505] = Sand
    while t < Time: 
        #print(max(Sandbox))
        too_high = np.nonzero(Sandbox > 3)[0]
        if len(too_high) == 0:
            break

        loc = too_high
        a = loc > 2*Xdim-1
        b = loc%Xdim>2
        c = loc%Xdim<(Xdim-2)
        d = loc<Xdim*(Xdim-2)
        loc = loc[a & b & c & d]
        
        pile_height = Sandbox[loc]
        new_height = pile_height % 4
        Sandbox[loc] = new_height
        spill_height = (pile_height - new_height) / 4       
        
        
        Sandbox[loc+1] += spill_height
        Sandbox[loc-1] += spill_height
        Sandbox[loc+Ydim] += spill_height
        Sandbox[loc-Ydim] += spill_height
        t+=1
    print(max(Sandbox))
    

#%% RUN
topple(Sandbox,Time,Sand)    
show(Sandbox)  
    
#%%    
def gettopplers(Sandbox):
    concern = Sandbox.reshape(Xdim,Ydim)[(Xdim-1):, (Ydim-1):]
    return concern
    #np.arange(len(Sandbox)).reshape(Xdim,Ydim)[1:-1, 1:-1].flatten()
    
    
    
    