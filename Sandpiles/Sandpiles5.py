'''
Sandpiles (re-write)
https://en.wikipedia.org/wiki/Abelian_sandpile_model
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,12
from scipy import ndimage

#%% SETUP
'''
One dict specidies the corrdinates and we only add to log if they are part of pile
Will get harder to check every single one for topple factor
So maybe keep two dicts

'''
#%% SHOW

def view(sandict):
    xcord = []
    ycord = []
    h = []
    
    for key in sandbox:
        i,j = key
        xcord += [i]
        ycord += [j]
        h += [sandbox[(i,j)]]
    
    xcord = np.array(xcord) - min(xcord)
    ycord = np.array(ycord) - min(ycord)
    arena = [[0 for ax in range(max(ycord)+1)] for ay in range(max(xcord)+1)]
    
    for p in range(len(xcord)):
        arena[xcord[p]][ycord[p]] = h[p]
    
    plt.imshow(arena, interpolation = 'none', cmap ='hot')
    plt.show()
        
#%%

sandbox = {(0,0):4**6}
toppler = [(0,0)]
time = 1000000

for t in range(time):
    if len(toppler) == 0:
        break
    
    i,j = toppler[0]
    del toppler[0]
    sand = sandbox[(i,j)]
    if sand == 0:
        continue
    
    sandbox[(i,j)] = sandbox[(i,j)]
    
    if (i+1,j) in sandbox:
        sandbox[(i+1,j)] += sand/4
    else:
        sandbox[(i+1,j)] = sand/4
    
    if (i-1,j) in sandbox:
        sandbox[(i-1,j)] += sand/4
    else:
        sandbox[(i-1,j)] = sand/4
        
    if (i,j+1) in sandbox:
        sandbox[(i,j+1)] += sand/4
    else:
        sandbox[(i,j+1)] = sand/4            
        
    if (i,j-1) in sandbox:
        sandbox[(i,j-1)] += sand/4
    else:
        sandbox[(i,j-1)] = sand/4  
        
        
    
    if sandbox[(i+1,j)] > 3:
        toppler += [(i+1,j)]
    if sandbox[(i-1,j)] > 3:
        toppler += [(i-1,j)]        
    if sandbox[(i,j+1)] > 3:
        toppler += [(i,j+1)]
    if sandbox[(i,j-1)] > 3:
        toppler += [(i,j-1)]            
#        
    if t%10000 == 0:
        plt.title(len(sandbox.keys()))
        view(sandbox)
        print(t)
        

view(sandbox)
#%%



