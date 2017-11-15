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
sandboxX = 250
sandboxY = 250
sandbox = [[0 for i in range(sandboxX)] for j in range(sandboxY)]
sandbox[sandboxX/2][sandboxY/2] = 1000000
sandbox[sandboxX/2 + 1][sandboxY/2] = 0
sandbox = np.array(sandbox)

sliders = {(sandboxX/2,sandboxY/2):True,(sandboxX/2+1,sandboxY/2):True}

for time in range(4000):  
    if time%1 == 0:
        ax = plt.imshow(sandbox,interpolation='none',cmap='hot')#,vmin=0,vmax=100000)
        plt.title(str(time))
#        plt.savefig('latest')
#        plt.clf()
#        plt.cla()
        plt.show()
        print(time)

    log = sliders.keys()
#    slidedex = np.random.randint(len(log))
    
    for slidedex in np.arange(len(log)):
        epicenter = log[slidedex]
        i,j = epicenter
        sand = sandbox[i][j]
        
        sandbox[i+1][j] += sand/4
        sandbox[i][j+1] += sand/4
        sandbox[i-1][j] += sand/4
        sandbox[i][j-1] += sand/4
        sandbox[i][j] = 0
        
        if sandbox[i+1][j] > 4:
            sliders[(i+1,j)] = True
        if sandbox[i-1][j] > 4:
            sliders[(i-1,j)] = True
        if sandbox[i][j+1] > 4:
            sliders[(i,j+1)] = True
        if sandbox[i][j-1] > 4:
            sliders[(i,j-1)] = True


        if len(log) < 1:
            break
#%%




