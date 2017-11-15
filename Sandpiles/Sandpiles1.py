'''
Sandpiles (optimized)
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,12
from scipy import ndimage


def gravity(sandbox):
    tippingpoint = np.nonzero(np.array(sandbox)>4)
    
    cuspval = len(tippingpoint[0])     
    epicenter = np.random.randint(cuspval)
    i,j = tippingpoint[0][epicenter], tippingpoint[1][epicenter]          

    sand = sandbox[i][j]
    sandbox[i][j] = sand/5
    sandbox[i+1][j] += sand/5
    sandbox[i][j+1] += sand/5
    sandbox[i-1][j] += sand/5
    sandbox[i][j-1] += sand/5
    

#%%
sandboxX = 150
sandboxY = 150
sandbox = [[0 for i in range(sandboxX)] for j in range(sandboxY)]
sandbox[sandboxX/2][sandboxY/2] = 50000
sandbox[sandboxX/2 + 1][sandboxY/2] = 50000
sandbox = np.array(sandbox)

for i in range(50000):    
    gravity(sandbox)
    
plt.imshow(sandbox,interpolation='none',cmap='hot')
plt.show()







