'''
Sandpiles (re-write)
https://en.wikipedia.org/wiki/Abelian_sandpile_model

Take to 1d array and get recursive

I HAVE A FEELING this is wrong, am I counting for second order effects?
Well, yes you are, but you are calling the function several times on the 
same cells.

//NOT WORKING - IT SEEMS//

'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 10,10

#%% SETUP
Xdim = 200
Ydim = 200
Sandbox = np.array([0 for i in range(Xdim*Ydim)])
Sand = 20000
#%% DISPLAY
def show(Sandbox,Sand = Sand):
    Sandbox2D = Sandbox.reshape(Xdim,Ydim)
    plt.matshow(Sandbox2D,cmap='hot',vmin = 0, vmax = 3)
    plt.title('Zero for {0} grains'.format(Sand))
    plt.show()
    

#%% TOPPLE    
def setup(Sandbox,Sand,Ydim=Ydim,Xdim=Xdim):
    center = len(Sandbox)/2 + Xdim/2
    Sandbox[center] = Sand
    
    topple(Sandbox, center, 0)
    
    show(Sandbox)

def topple(Sandbox, loc, spillover):
    new_height = Sandbox[loc] + spillover
    
    if new_height < 4:
        Sandbox[loc] = new_height
    else:
        new_spilled_height = new_height % 4
        Sandbox[loc] = new_spilled_height
        spillover = (new_height - new_spilled_height)/4
        topple(Sandbox, loc + 1, spillover)
        topple(Sandbox, loc - 1, spillover)
        topple(Sandbox, loc + Ydim, spillover)
        topple(Sandbox, loc - Ydim, spillover)
    
    
    
#%% RUN
setup(Sandbox,Sand) 
    
    
    
    
    
    
    