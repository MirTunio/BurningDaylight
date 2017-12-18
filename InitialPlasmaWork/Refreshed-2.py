#borrowed BC setting from Refreshed-1.py, now start again#scratch
#lets see how far you can carry this reshaped list thing without going matrix

import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
from scipy import ndimage
rcParams['figure.figsize'] = 7,7

#Diagnostic Tools
def draw():
    return test.reshape(slen,slen)
def draw2():
    return np.array(np.arange(0,size)).reshape(slen,slen)
def draw3(mat):
    m = np.matrix(mat.reshape(slen,slen))
    plt.imshow(m,interpolation='nearest')
def sumch():
    mat = np.matrix(rhog.reshape(slen,slen))
    return np.sum(mat[1:(slen-1),1:(slen-1)])
def drawtrons():
    plt.plot(posx,posy,marker='.',linewidth = 0,ms=50,alpha=-0.9)
    plt.xlim(0,blen)
    plt.ylim(0,blen)
    plt.show()

#Parameters
blen = 100.0 #size of box
slen = 10 #set number grid points along length of box (2 on either end are mirrored)
size = slen**2 #area of box, with mirrored top and bottom
Ng = (slen-2)**2 #number of grid points
clen = blen/(slen-2) # size of cell
#rhog = np.array(np.arange(0,size),dtype='float64') #the grid #diagnostic version
rhog = np.zeros(size,dtype='float64') #the grid for rho


DT = 0.2 #time step
Np = 1000 #number of particles

#Setting Up Corners of rho grid, not nescessary but good for debugging
rhog[0] = 99
rhog[slen-1] = 99
rhog[size - slen] = 99
rhog[size-1] = 99

#Mirrors elements of the grid to effectively apply periodic boundary conditions
def applyBC(mat):
    #setting top and bottom
    mat[1:slen-1] = mat[size - 2*slen+1:size - slen -1]
    mat[size - slen + 1:size-1] = mat[slen+1:2*slen-1]
    #setting sides
    for i in np.arange(1,slen-1):
        mat[slen*i] = mat[slen*(i+1)-2]
    for i in np.arange(1,slen-1):
        mat[slen*(i+1)-1] = mat[slen*i+1]
    
#Initialization:
posx = np.random.rand(Np)*blen #x coordinate of particles
posy = np.random.rand(Np)*blen #y coordinate of particles

#posy = 60*np.ones(Np)
#posx = 80*np.ones(Np)

#drawtrons()

def distrho():
    xinter = np.floor((posx/blen)*(slen-2))
    winter = np.floor(((blen - posy)/blen)*(slen-2)) #careful, flipped so showell
    axter = (slen + 1 + xinter+slen*winter).astype('int')
    for c in axter:
        rhog[c] = rhog[c]+40
    
print(distrho())

draw3(rhog)
plt.show()
drawtrons()

#Pot solve

phig = np.array(np.arange(0,size),dtype='float64')
rhocoeff = np.fft.fft2(rhog.reshape(slen,slen)[1:(slen-1),1:(slen-1)])
phicoeff = np.zeros([size-2,size-2],'float64')

Ex = np.zeros([slen-2,slen-2])
Ey =  np.zeros([slen-2,slen-2])

for i in xrange(slen-2):
    for j in xrange(slen-2):
        phicoeff[i][j] = rhocoeff[i][j]/((i**2+j**2)*np.pi**2)

phi = np.real(np.fft.ifft2(phicoeff[1:(slen-1),1:(slen-1)]))

me = np.matrix(phi)
plt.imshow(me,interpolation='nearest')

phigs = np.zeros([slen,slen])
phigs[1:(slen-1),1:(slen-1)] = phi
phigf = phigs.flatten()
applyBC(phigf)

u = np.matrix(phigf.reshape(10,10))
plt.imshow(u,interpolation='nearest')


up = phigf.reshape(10,10)

for i in np.arange(1,slen-1):
    for j in np.arange(1,slen-1):
        Ex[i-1][j-1] = (up[i-1][j]-up[i+1][j])/(2*clen)
        Ey[i-1][j-1] = (up[i][j-1]-up[i][j+1])/(2*clen)

q = 1

#for i in np.arange(Np)
#Fx = Ex[np.floor((posx/blen)*(slen-2))]]*q
#Fy = Ey[posy[np.floor((posy/blen)*(slen-2))]]*q

vx = np.zeros(Np)
vy = np.zeros(Np)

vx = Fx*DT+vx
vy = Fy*DT+vy

posx = posx + vx*DT
posy = posy + vy*DY

        
#initialize
#distrho()
#applyBC
#solve V
#solve E
#solve F
#move particles (posx,posy update)
#repeat

# 4*v[i][j] - v[i+1][j] - v[i-1][j] - v[i][j+1] - v[i][j-1]  == (-1*clen**2)*rho[i][j]
# v[i][j] = (1/4)*(v[i+1][j] + v[i-1][j] + v[i][j+1] + v[i][j-1] + (-1*clen**2)*rho[i][j])








    