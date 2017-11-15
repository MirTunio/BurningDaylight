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
time = 50000
sandbox[X/2][Y/2] = 4

topplers = set()
topplers.add((X/2,Y/2))

def topple(coord):
    i,j = coord
    sandbox[i][j] = 0
    sandbox[i+1][j] += 1
    sandbox[i][j+1] += 1
    sandbox[i-1][j] += 1
    sandbox[i][j-1] += 1
    
    if sandbox[i+1][j] > 3:
        topplers.add((i+1,j))

    if sandbox[i-1][j] > 3:
        topplers.add((i-1,j))        

    if sandbox[i][j+1] > 3:
        topplers.add((i,j+1))
        
    if sandbox[i][j-1] > 3:
        topplers.add((i,j-1)) 
        
    topplers.remove((i,j))
        
for T in range(time): 
#    plt.matshow(sandbox,interpolation='none',cmap='hot')   
#    plt.show()
#    print('')    
    
    if not(any(topplers)):
        side = len(sandbox)
        sandbox[side/2][side/2] = 4
        topplers.add((side/2,side/2))
        
    for coord in topplers.copy():
        topple(coord)

'''
    topple takes the most time, but called 111930 times, 0.000 per call...
    len of dict similar case... see where that is coming up 
'''
