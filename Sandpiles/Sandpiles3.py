'''
Sandpiles (experimental 2)
https://en.wikipedia.org/wiki/Abelian_sandpile_model
'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,12
from scipy import ndimage


#%%
sandboxX = 5
sandboxY = 5
sandbox = [[0 for i in range(sandboxX)] for j in range(sandboxY)]
sandbox[sandboxX/2][sandboxY/2] = 36
#sandbox[sandboxX/2 + 1][sandboxY/2] = 10000000000000
sandbox = np.array(sandbox)

sliders ={}
for i in range(sandboxX):
    for j in range(sandboxY):
        sliders[(i,j)] = False

sliders[(sandboxX/2,sandboxY/2)] = True

for time in range(10):
    print(sliders)
    log = sliders.keys()

    if time%1 == 0:
        ax = plt.imshow(sandbox,interpolation='none',cmap='hot')#,vmin=0,vmax=100000)
        plt.title(str(time))
#        plt.savefig('latest')
#        plt.clf()
#        plt.cla()
        plt.show()
        print(time)
        
    for slidedex in np.arange(len(log)):
        epicenter = log[slidedex]
        if sliders[epicenter] == False:
            break
        i,j = epicenter
        sand = sandbox[i][j]
        sandbox[i][j] = 0
        sandbox[i+1][j] += sand/4
        sandbox[i][j+1] += sand/4
        sandbox[i-1][j] += sand/4
        sandbox[i][j-1] += sand/4
        
        if sandbox[i+1][j] > 4:
            sliders[(i+1,j)] = True
        if sandbox[i-1][j] > 4:
            sliders[(i-1,j)] = True
        if sandbox[i][j+1] > 4:
            sliders[(i,j+1)] = True
        if sandbox[i][j-1] > 4:
            sliders[(i,j-1)] = True
            
        if sand/4 < 4:
            sliders[epicenter] = False
  

#%%




