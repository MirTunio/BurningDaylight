'''
Sandpiles
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,12

def gravity(sandbox):
    I,J = np.shape(sandbox)
    tippingpoint = []
    
    for i in range(1,I-1):
        for j in range(1,J-1):
            if sandbox[i][j] > 4:
                tippingpoint += [(i,j)]
                
    cuspval = len(tippingpoint)       
    if cuspval > 1:     
        i,j = tippingpoint[np.random.randint(cuspval)]           
    else:
        i,j = 50,50
        
    sand = sandbox[i][j]
    sandbox[i][j] = sand/4
    sandbox[i+1][j] += sand/4
    sandbox[i][j+1] += sand/4
    sandbox[i-1][j] += sand/4
    sandbox[i][j-1] += sand/4
    return sandbox
    

#%%
sandbox = [[0 for i in range(100)] for j in range(100)]
sandbox[50][50] = 10000000
iterations = 0

while iterations < 10000:
    #plt.imshow(sandbox,interpolation='none')
    #plt.show()
    
    avalanche = gravity(sandbox)
    iterations += 1
    print(iterations)
    

plt.imshow(sandbox,interpolation='none')
plt.show()