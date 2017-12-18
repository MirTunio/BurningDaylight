#And we start from the top
#Attempted to solve matrix probelm


import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
from scipy import linalg as lg
#import scipy scipy.sparse.linalg.lsqr
from scipy.sparse.linalg import lsqr as solve

rcParams['figure.figsize'] = 13,13

#---------------------------------
# 1D particle model
# PIC model
# USING HOCKNEY
# Moving to a self combined method, with grids borrowed from
# before, with boris pusher implementation in 2D
#---------------------------------
# IDEA:
# Lets start this from the top using what you know, off hand
# Code as far as you can go, then look at reference
# 2D model
# Electrostaic regime
# If you are looking at bulk properties, boundary conditions dont matter
# --------------------------------
# Perflogs:
# initialize till distrho: 04.88s with plots
# initialize till distrho: 77.5ms no plots 
# initialize till distrho: 59.7ms no plots
# initialize till phi solve 71.3ms no plots
#
#
#

rho0 = 25     # bacground charge density per grid point
e = -5        # charge of electron
Te = 1          #Need for poisson later?
epso = 8.854*10**-12		
K = 1.381*10**-23

# 11x11 GRID
# GRID object will hold information about rho and E field at each GP
# So 11x11 grid of tuples OR two 100 by 100 grids, I like this better
SpaceSize = 100
Gsize = 12.
Np = 605

# Initialize the grid
rho = np.zeros((Gsize,Gsize))+rho0
phi = np.zeros((Gsize,Gsize))
E = np.zeros((Gsize,Gsize))

#Initialize particles
posx = np.random.rand(Np)*SpaceSize
posy = np.random.rand(Np)*SpaceSize
# First plot of particles
#for i in np.arange(len(posx)):
#    plt.xlim(0,SpaceSize)
#    plt.ylim(0,SpaceSize)
#    plt.plot(posx[i],posy[i],marker = 'x',linewidth = 0,color = 'black')
    #plt.plot(rho,marker = 'x',linewidth = 0,color = 'black')
#plt.show()

#Now we define interpolation scheme
def distrho(rho):
    div = (SpaceSize/(Gsize-1))
    #Using a simple interp, could use weights based on areas
    for i in xrange(len(posx)):
        rho[np.round(posx[i]/div)][np.round(posy[i]/div)] += e #simple, fakin fast
    #Setting Boundary conditions
    
    #rho = rho/100.0
print rho
plt.imshow(rho,cmap='hot')
plt.colorbar()
plt.show() 

#distrho(rho)

print rho
plt.imshow(rho,cmap='hot')
plt.colorbar()
plt.show()   

print('netq: '+ str(sum(sum(rho))))











































#---------------------------
#Poisson Matrix

A = np.matrix([[4,-1,0],[-1,4,-1],[0,-1,4]])
B = -1*np.identity(3)
C = np.zeros((3,3))

pmat = np.bmat(
        'A,B'  +',C'*46+';'+
        'B,A,B'+',C'*45+';'+
'C,'*1+ 'B,A,B'+',C'*44+';'+
'C,'*2+ 'B,A,B'+',C'*43+';'+
'C,'*3+ 'B,A,B'+',C'*42+';'+
'C,'*4+ 'B,A,B'+',C'*41+';'+
'C,'*5+ 'B,A,B'+',C'*40+';'+
'C,'*6+ 'B,A,B'+',C'*39+';'+
'C,'*7+ 'B,A,B'+',C'*38+';'+
'C,'*8+ 'B,A,B'+',C'*37+';'+
'C,'*9+ 'B,A,B'+',C'*36+';'+
'C,'*10+'B,A,B'+',C'*35+';'+
'C,'*11+'B,A,B'+',C'*34+';'+
'C,'*12+'B,A,B'+',C'*33+';'+
'C,'*13+'B,A,B'+',C'*32+';'+
'C,'*14+'B,A,B'+',C'*31+';'+
'C,'*15+'B,A,B'+',C'*30+';'+
'C,'*16+'B,A,B'+',C'*29+';'+
'C,'*17+'B,A,B'+',C'*28+';'+
'C,'*18+'B,A,B'+',C'*27+';'+
'C,'*19+'B,A,B'+',C'*26+';'+
'C,'*20+'B,A,B'+',C'*25+';'+
'C,'*21+'B,A,B'+',C'*24+';'+
'C,'*22+'B,A,B'+',C'*23+';'+
'C,'*23+'B,A,B'+',C'*22+';'+
'C,'*24+'B,A,B'+',C'*21+';'+
'C,'*25+'B,A,B'+',C'*20+';'+
'C,'*26+'B,A,B'+',C'*19+';'+
'C,'*27+'B,A,B'+',C'*18+';'+
'C,'*28+'B,A,B'+',C'*17+';'+
'C,'*29+'B,A,B'+',C'*16+';'+
'C,'*30+'B,A,B'+',C'*15+';'+
'C,'*31+'B,A,B'+',C'*14+';'+
'C,'*32+'B,A,B'+',C'*13+';'+
'C,'*33+'B,A,B'+',C'*12+';'+
'C,'*34+'B,A,B'+',C'*11+';'+
'C,'*35+'B,A,B'+',C'*10+';'+
'C,'*36+'B,A,B'+',C'*9+';'+
'C,'*37+'B,A,B'+',C'*8+';'+
'C,'*38+'B,A,B'+',C'*7+';'+
'C,'*39+'B,A,B'+',C'*6+';'+
'C,'*40+'B,A,B'+',C'*5+';'+
'C,'*41+'B,A,B'+',C'*4+';'+
'C,'*42+'B,A,B'+',C'*3+';'+
'C,'*43+'B,A,B'+',C'*2+';'+
'C,'*44+'B,A,B'+',C'*1+';'+
'C,'*45+'B,A,B'+';'+
'C,'*46+'B,A')
#------------------------------
#test case for solver:
testmat = np.bmat([[A,B,C],[B,A,B],[C,B,A]])
testb = [25,50,150,0,0,50,0,0,25]
#sols [18.75, 37.5, 56.25, 12.5, 25. ,37.5, 6.25, 12.5,18.75]
#------------------------------

















#Computing Potentials
plt.imshow(phi,cmap='hot')
plt.colorbar()
plt.show()

sol = solve(pmat,rho.flatten())[0]
phi = np.reshape(sol,(12,12))

plt.imshow(phi,cmap='hot')
plt.colorbar()
plt.show()



















