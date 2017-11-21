'''
Sandpiles (re-write)
https://en.wikipedia.org/wiki/Abelian_sandpile_model

Life, living organisms are on the edge of chaos. 
Living between ordered and chaotic regimes, at a critical point. 
('This compromise between order and surpirse - appear best able
to coordinate complex activities and best able to evolve as well'
- Stuart Kauffman)
The sandpile model demmonstrates how such critical points arise
in nature.Indeed, how these critical points self-organize.

Beautiful, life in a grain of sand. 
'''



'''
Take to 1d array and lose the 'topple' function. LETS GET EFFIECIENT
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 30,30

#%% SETUP
Xdim = 1500
Ydim = 1500
Sandbox = np.array([0 for i in range(Xdim*Ydim)])
Sand = 2**30
Time = 100000000000
index = np.arange(len(Sandbox)).reshape(Xdim,Ydim)[1:-1, 1:-1].flatten()
#%% DISPLAY
def show(Sandbox,Sand = Sand):
    Sandbox2D = Sandbox.reshape(Xdim,Ydim)
    plt.matshow(Sandbox2D,cmap='plasma',vmin = 0, vmax = 3)
    plt.title('Zero for {0} grains'.format(Sand))
    plt.show()
    

#%% TOPPLE
'''
Attempt to get rid of the need to search the whole matrix each iteratiion
'''
def topple(Sandbox,Time,Sand,Ydim=Ydim,Xdim=Xdim):
    t = 0
    Sandbox[len(Sandbox)/2 + Xdim/2] = Sand
    while t < Time: 
        #print(max(Sandbox))
        too_high = np.nonzero(Sandbox > 3)
        if len(too_high[0]) < 1:
            break
        loc = too_high[0]
        pile_height = Sandbox[loc]
        new_height = pile_height % 4
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
    
    
    
    
    
    
    
