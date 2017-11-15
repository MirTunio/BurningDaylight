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
time = 10000
sandbox[X/2][Y/2] = 4

topplers = {(X/2,Y/2):''}

def topple(coord):
    i,j = coord
    sandbox[i][j] = 0
    sandbox[i+1][j] += 1
    sandbox[i][j+1] += 1
    sandbox[i-1][j] += 1
    sandbox[i][j-1] += 1
    
    if sandbox[i+1][j] > 3:
        topplers[(i+1,j)] = ''

    if sandbox[i-1][j] > 3:
        topplers[(i-1,j)] = ''        

    if sandbox[i][j+1] > 3:
        topplers[(i,j+1)] = ''
        
    if sandbox[i][j-1] > 3:
        topplers[(i,j-1)] = '' 
        
    del topplers[(i,j)]
        
for T in range(time):
    if not(any(topplers)):
        sandbox[len(sandbox)/2][len(sandbox)/2] = 4
        topplers[(len(sandbox)/2,len(sandbox)/2)] = True
        
    for coord in topplers.keys():
        topple(coord)

'''
    topple takes the most time, but called 111930 times, 0.000 per call...
    len of dict similar case... see where that is coming up 
'''

plt.matshow(sandbox,interpolation='none',cmap='hot')