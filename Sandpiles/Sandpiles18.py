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
Xdim = 300
Ydim = 300
Sandbox = np.array([0 for i in range(Xdim*Ydim)])
Sand = 2**20
Time = 4000
ref =  np.arange(0,Xdim*Ydim).reshape(Xdim,Ydim)
quarter = ref[Xdim/2-1:,Ydim/2-1:].flatten()
dex = np.arange(0,len(Sandbox))[quarter]

#%% Mapping quarters
ref2 = ref[::-1,:]
flipupmap = {}
for i in range(len(ref)):
    for j in range(len(ref[0])):
        flipupmap[ref[i][j]] = ref2[i][j]
        
ref3 =  ref[:,::-1]      
flipsidemap = {}
for i in range(len(ref)):
    for j in range(len(ref[0])):
        flipsidemap[ref[i][j]] = ref3[i][j]
        
#%% DISPLAY
def show(Sandbox,Sand = Sand):
    Sandbox2D = Sandbox.reshape(Xdim,Ydim)
    plt.matshow(Sandbox2D,cmap='hot',vmin = 0, vmax = 3)
    plt.title('Zero for {0} grains'.format(Sand))
    plt.show()
    
    
#%% TOPPLE
'''
Well, I tried to be clever and nonzero a quarter and map. There is something
here but not so clear!
Need to use a geometric trick
'''
def topple(Sandbox,Time,Sand,Ydim=Ydim,Xdim=Xdim):
    t = 0
    Sandbox[len(Sandbox)/2 + Xdim/2] = Sand
    #Sandbox[505] = Sand
    while t < Time: 
        too_high = np.extract(Sandbox[quarter] > 3,dex)
        too_high = np.append(too_high, [flipupmap[k] for k in too_high])
        too_high = np.append(too_high, [flipsidemap[k] for k in too_high])
        
        if len(too_high) == 0:
            break
        loc = too_high
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
    
    
    
    