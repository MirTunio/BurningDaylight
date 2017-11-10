#Linear iterative maps
#previous: binary
#next: quadratic

#NOTE: This is not algorithmically equivalent to the plotting method on right panes, I think

import numpy as np
from matplotlib import pyplot as plt

s0 = 1
statehist = np.array([s0]).astype('float64')

def staten():
    global statehist

    #constant
    ###statehist = np.append(statehist,statehist[-1:]) 
    
    #free motion
    ###v = 1
    ###statehist = np.append(statehist,statehist[-1:]+v)
    
    #multiplicative
    g = -0.5
    statehist = np.append(statehist,g*statehist[-1:])
    
    return statehist
    
def state():
    return statehist[-1:][0]
    
    
for i in np.arange(15):
    staten()
    

plt.plot(statehist)
plt.show()