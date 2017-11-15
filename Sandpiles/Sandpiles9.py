'''
Sandpiles (re-write)
https://en.wikipedia.org/wiki/Abelian_sandpile_model
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,12

#%%
X,Y = 5,5
sandbox = np.array([[0 for i in range(X)] for j in range(Y)]).astype('int8')
time = 1000000
sandbox[X/2][Y/2] = 4
topplers = [(X/2,Y/2)]

def getopplers(sandbox):
    a,b = np.nonzero(sandbox>3)
    return zip(a,b)    

def topple(coord):
    i,j = coord
    sandbox[i][j] = 0
    sandbox[i+1][j] += 1
    sandbox[i][j+1] += 1
    sandbox[i-1][j] += 1
    sandbox[i][j-1] += 1

for T in range(time):
    if T%10000 == 0:
        plt.matshow(sandbox,interpolation='none',cmap='hot')
        plt.show()
        print('Time: ' + str(T), 'Sand: '+ str(np.sum(sandbox)))#,str(np.shape(sandbox)),str(len(sandbox.nonzero()[0])))
        
            
    if len(topplers) == 0:
        sandbox[len(sandbox)/2][len(sandbox)/2] = 4
    
    topplers = getopplers(sandbox)
    for coord in topplers:
        topple(coord)

    if (sum(sandbox[0])>0) or (sum(sandbox[-1])>0) or (sum(sandbox[-1,:])>0) or (sum(sandbox[-1,:])>0):
        sandbox = np.lib.pad(sandbox,1,mode='constant')




