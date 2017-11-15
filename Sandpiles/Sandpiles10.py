'''
Sandpiles (re-write)
https://en.wikipedia.org/wiki/Abelian_sandpile_model
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,12

#%%
X,Y = 80,80
sandbox = np.array([[0 for i in range(X)] for j in range(Y)]).astype('int8')
time = 3000000
sandbox[X/2][Y/2] = 4
#topplers = [(X/2,Y/2)]

topplers = {(X/2,Y/2):True}

def topple(coord):
    i,j = coord
    sandbox[i][j] = 0
    sandbox[i+1][j] += 1
    sandbox[i][j+1] += 1
    sandbox[i-1][j] += 1
    sandbox[i][j-1] += 1
    
    if ((i+1,j) not in topplers) and sandbox[i+1][j] > 3:
        topplers[(i+1,j)] = True

    if ((i-1,j) not in topplers) and sandbox[i-1][j] > 3:
        topplers[(i-1,j)] = True        

    if ((i,j+1) not in topplers) and sandbox[i][j+1] > 3:
        topplers[(i,j+1)] = True
        
    if ((i,j-1) not in topplers) and sandbox[i][j-1] > 3:
        topplers[(i,j-1)] = True 
        
    del topplers[(i,j)]
        
for T in range(time):            
    if len(topplers) == 0:
        sandbox[len(sandbox)/2][len(sandbox)/2] = 4
        topplers[(len(sandbox)/2,len(sandbox)/2)] = True
        
    for coord in topplers.keys():
        topple(coord)

'''
optimization profile says:
    when you ask for the keys of a dict - blashphemy
    
'''

plt.matshow(sandbox,interpolation='none',cmap='hot')


