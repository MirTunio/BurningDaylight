#Borrowing things from Refreshed-2.py and abstracting as I go
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
from scipy import ndimage
from collections import Counter
rcParams['figure.figsize'] = 7,7

#Parameters
#Arena
blen = 100.0 #size of box
slen = 30 #set number grid points along length of box (2 on either end are mirrored)
size = slen**2 #area of box, with mirrored top and bottom
Ng = (slen-2)**2 #number of grid points
clen = blen/(slen-2) # size of cell
Np = 1000  #number of particles

#Other
cycles = 3
DT = 0.2 #time step per cycle
q = -1


#Initializing Arrays
#charge
#rhog = np.array(np.arange(0,size),dtype='float64') #the grid #diagnostic version
rhog = np.zeros(size,dtype='float64') #the grid for rho
rhog[0] = 0
rhog[slen-1] = 0
rhog[size - slen] = 0
rhog[size-1] = 0
rhog = rhog.reshape(slen,slen)

#position of particles
pos = np.random.rand(Np)*((slen-2)**2+1) #index coordinate of particles
posx = np.random.rand(Np)*blen
posy = np.random.rand(Np)*blen
posinterx = np.zeros(Np)
posintery = np.zeros(Np)

#pos = np.ones(Np)*400
#posinter = np.zeros(Np)

#Potential
#phig = np.array(np.arange(0,size),dtype='float64').reshape(slen,slen)
phig = np.zeros(size,dtype='float64').reshape(slen,slen)

#Electric Field
Ex = np.zeros([slen,slen])
Ey =  np.zeros([slen,slen])

#Force
Fx = np.zeros(Np,dtype='float64')
Fy = np.zeros(Np,dtype='float64')

#Velocities
vx = np.zeros(Np)
vy = np.zeros(Np)


#def initialize():


def applyBClis(mat): #Takes a lis matrix and applies periodic BC, assuming it has blank buffer all around
    #setting top and bottom
    mat[1:slen-1] = mat[size - 2*slen+1:size - slen -1]
    mat[size - slen + 1:size-1] = mat[slen+1:2*slen-1]
    #setting sides
    for i in np.arange(1,slen-1):
        mat[slen*i] = mat[slen*(i+1)-2]
    for i in np.arange(1,slen-1):
        mat[slen*(i+1)-1] = mat[slen*i+1]
        
def applyBCmat(mat): #Takes a matrix and applies periodic BC, assuming it has blank buffer all around
    mat[0] = mat[slen-2]
    mat[slen-1] = mat[1]
    mat[1:slen-1,0] = mat[1:slen-1,slen-2]
    mat[1:slen-1,slen-1] = mat[1:slen-1,1]

def interp(): #interpolation scheme, this and below
    global posinterx,posintery
    posinterx = np.floor((posx/blen)*(slen-2))
    posintery = np.floor((posy/blen)*(slen-2))

    
def distrho(): #Charge distribution #V slow
    interp()
    rho0 = -1*(Np*q)/float(Ng)
    rhoacc = np.zeros([slen-2,slen-2])
    
    for i in np.arange(Np):
        rhoacc[posinterx[i],posintery[i]] += q
    
    rhoacc = rhoacc+rho0
    
    rhog[1:(slen-1),1:(slen-1)] = rhoacc

distrho()
applyBCmat(rhog)
draw3(rhog)
        
def computeV(): #I think the math is on point..
    #FFT the charge distribution
    rhocoeff = np.fft.fft2(rhog[1:(slen-1),1:(slen-1)])
    phicoeff = np.zeros([size-2,size-2],'float64')
    
    for i in xrange(slen-2):
        for j in xrange(slen-2):
            phicoeff[i][j] = rhocoeff[i][j]/((i**2+j**2)*np.pi**2)
    phig[1:(slen-1),1:(slen-1)] = np.real(np.fft.ifft2(phicoeff[1:(slen-1),1:(slen-1)]))
    #return phi

computeV()
applyBCmat(phig)
draw3(phig)
        

#up = phigf.reshape(10,10)

def computeE():
    for i in np.arange(1,slen-1):
        for j in np.arange(1,slen-1):
            Ex[i][j] = (phig[i-1][j]-phig[i+1][j])/(2*clen)
            Ey[i][j] = (phig[i][j-1]-phig[i][j+1])/(2*clen)
        
computeE()
applyBCmat(Ex)
applyBCmat(Ey)

draw3(Ex)     

def computeF():
    culledEx = Ex[1:(slen-1),1:(slen-1)]
    culledEy = Ey[1:(slen-1),1:(slen-1)]
    
    for i in xrange(Np):
        posx = posinter[i]%(slen-2) #x grid coord
        posy = posinter[i]/(slen-2) #y grid coord
        #print(posinter[i])
        #print(posx,posy)
        Fx[i] = Ex[posx,posy]
        Fy[i] = Ey[posx,posy]

computeF()
 
def updatevel():
    global vx,vy
    vx = vx + Fx*DT
    vy = vy + Fy*DT

updatevel()

def updatepos():
    global posx,posy
    posx = posx + vx*DT
    posy = posy + vy*DT
    
updatepos()
        

        
        
        
        
        
        
 #Diagnostic Tools
def draw():
    return test.reshape(slen,slen)
def draw2():
    return np.array(np.arange(0,size)).reshape(slen,slen)
def draw3(mat):
    m = np.matrix(mat.reshape(slen,slen))
    plt.imshow(m,interpolation='nearest')
    plt.show()
def sumch():
    mat = np.matrix(rhog.reshape(slen,slen))
    return np.sum(mat[1:(slen-1),1:(slen-1)])
def drawtrons():
    plt.plot(posx,posy,marker='.',linewidth = 0,ms=50,alpha=-0.9)
    plt.xlim(0,blen)
    plt.ylim(0,blen)
    plt.show()       
def chgcons():
    print(np.sum(rhog[1:(slen-1),1:(slen-1)]))