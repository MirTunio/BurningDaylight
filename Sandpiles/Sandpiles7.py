'''
Sandpiles (re-write)
https://en.wikipedia.org/wiki/Abelian_sandpile_model
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,12
from scipy import ndimage

#%%
X,Y = 5,5
sandbox = np.array([[0 for i in range(X)] for j in range(Y)])
time = 1000000
sandbox[X/2][Y/2] = 4
topplers = [(X/2,Y/2)]
topnew = []

def getopplers(sandbox):
    pretop = np.nonzero(sandbox>3)
    
    if len(pretop[0]) == 1:
        ex,ey = pretop
        return [(ex[0],ey[0])]
    else:
        topx,topy = pretop
        return [(topx[i],topy[i]) for i in range(len(topx))]
    
def topple(coord):
    i,j = coord
    sandbox[i][j] = 0
    sandbox[i+1][j] += 1
    sandbox[i][j+1] += 1
    sandbox[i-1][j] += 1
    sandbox[i][j-1] += 1
    

for T in range(time):
    if T%10000 ==0:
        plt.title(T)
        plt.imshow(sandbox,interpolation='none',cmap='hot')
        plt.show()
        print(np.sum(sandbox))
            
    if len(topplers) == 0:
        sandbox[len(sandbox)/2][len(sandbox)/2] = 4
    
    topplers = getopplers(sandbox)
    for coord in topplers:
        topple(coord)

    if (np.max(np.nonzero(sandbox))+2) > len(sandbox):
        sandbox = np.lib.pad(sandbox,1,mode='constant')

    

#%%
    
