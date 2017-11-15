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
X,Y = 21,21
sandbox = [[0 for i in range(X)] for j in range(Y)]
time = 74
sandbox[X/2][Y/2] = 4
topplers = [(X/2,Y/2)]
topnew = []

for T in range(time):
    
    #if T%10 == 0:
    #    plt.imshow(sandbox,interpolation='none',cmap='hot')
    #    plt.show()
    #    print(T)
    print(np.matrix(sandbox))
    print(topplers)
    print(T)
    print('######')
        
        
    if len(topplers) == 0:
        sandbox[X/2][Y/2] = 4
        topplers = [(X/2,Y/2)]
        
    for mee in range(len(topplers)):
        topple = topplers[mee]
        i,j = topple
        sandbox[i][j] = 0
        sandbox[i+1][j] += 1
        sandbox[i][j+1] += 1
        sandbox[i-1][j] += 1
        sandbox[i][j-1] += 1

        if sandbox[i+1][j] > 3:
            topnew += [(i+1,j)]
        if sandbox[i-1][j] > 3:
            topnew += [(i-1,j)]
        if sandbox[i][j+1] > 3:
            topnew += [(i,j+1)]
        if sandbox[i][j-1] > 3:
            topnew += [(i,j-1)]
          
    print(topplers)
    print('#########################')
    topplers = topnew
    topnew = []
    

#%%
    
