#Second iteration of test1 code

import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from scipy import integrate

rcParams['figure.figsize'] = 6,4

# Test case:
gridtest = np.arange(-30,30,1)
xtest    = (np.random.rand(10)*60)-30
qtest    = np.ones(10)
dx = 1

# Params:
k = 1
# Shape function:
def S(dist):
    return np.max([0,1-np.abs(dist)/dx])

# On Grid, general function to compute values of functions on grid points using above interp.
def oG(grid,xlocs,xqs,oGPfunc):
    temp = np.zeros(len(grid))
    for i in np.arange(len(grid)):
        temp[i] = oGPfunc(grid[i],xlocs,xqs)
    return temp  
    
# ---------------------------------
# Charge density at grid point:
def CDoGP(x_j,xlocs,xqs): #x_j = grid point, xlocs = coord of charges and corresp charge xqs
    temp = 0
    for i in np.arange(len(xlocs)):
        temp+= S(x_j-xlocs[i])*xqs[i]
    return temp
    
# Charge density on grid:
def CDoG(grid,xlocs,xqs):
    return oG(grid,xlocs,xqs,CDoGP)

#def CDinterp(x):
    #check which bin x is in
    #return bin func
# ---------------------------------
# Something TERRIBLY wrong here, why is it blowing up, you need define interp in charge dist better*
# Electric field on grid point:
def EFoGP(x_j,xlocs,xqs):
    CD = S(x_j-xlocs[i])*xqs[i]
    DIST = [(x_j) for GP in gridtest]
    return integrate.trapz((k*CD)/np.square(DIST))
 
# Electric field on grid:
def EFoG(grid,xlocs,xqs):
    return oG(grid,xlocs,xqs,EFoGP)

# ---------------------------------
    
# Plotting CDoG for test case:    
plt.plot(gridtest,CDoG(gridtest,xtest,qtest),marker = 'o', ms = 5, linewidth=0)
plt.plot(xtest,np.ones(len(xtest))*0.05,marker = 'x',linewidth = 0)
plt.show()

# Plotting EFoG for test case:
plt.plot(gridtest,EFoG(gridtest,xtest,qtest),marker = 'o', ms = 5, linewidth=0)
plt.show()





