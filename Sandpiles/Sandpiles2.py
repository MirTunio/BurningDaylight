'''
Sandpiles (experimental 1)
https://en.wikipedia.org/wiki/Abelian_sandpile_model
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,12
from scipy import ndimage


#%%
sandboxX = 150
sandboxY = 150
sandbox = [[0 for i in range(sandboxX)] for j in range(sandboxY)]
sandbox[sandboxX/2][sandboxY/2] = 1000000
sandbox[sandboxX/2 + 1][sandboxY/2] = 1000000
sandbox = np.array(sandbox)

for i in range(200000):    
    tippingpoint = np.nonzero(np.array(sandbox)>4)
    
#    cuspval = len(tippingpoint[0])     
#    if cuspval == 0:
#        print(i)
#        break
#    else:
#        epicenter = np.random.randint(cuspval)
#        
#    i,j = tippingpoint[0][epicenter], tippingpoint[1][epicenter]    
    i,j = tippingpoint[0][1], tippingpoint[1][1]     

#    sand = sandbox[i][j]
    sand = sandbox[i][j]
    sandbox[i][j] = sand/5
    sandbox[i+1][j] += sand/5
    sandbox[i][j+1] += sand/5
    sandbox[i-1][j] += sand/5
    sandbox[i][j-1] += sand/5
  
plt.imshow(sandbox,interpolation='none',cmap='hot')
plt.show()







