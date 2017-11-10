#Seems to be working
#Needs to be optimized (broadcast and iron out edge case handling with skill)
#and made ready for barrage of test cases (phase space plots must.)
#make ext plot live updat//ed
#WINNER
#V.Buggy though


#Borrowing things from Refreshed-2.py and abstracting as I go
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
from collections import Counter

rcParams['figure.figsize'] = 6,6

#Parameters
#Arena
blen = 1000 #size of box
slen = 70 #set number grid points along length of box (2 on either end are mirrored)
size = slen**2 #area of box, with mirrored top and bottom
Ng = (slen-2)**2 #number of grid points
clen = blen/(slen-2) # size of cell
Np = 100 #number of particles

#Other
iterations = 600
DT = 10 #time step per cycle
q = -10
m = 0.1

#Initializing Arrays
#charge
#rhog = np.array(np.arange(0,size),dtype='float64') #the grid #diagnostic version
rhog = np.zeros(size,dtype='float64') #the grid for rho
rhog[0] = 0
rhog[slen-1] = 0
rhog[size - slen] = 0
rhog[size-1] = 0
rhog = rhog.reshape(slen,slen)
rho0 = -1*(Np*q)/float(Ng)

#position of particles
#Random
posx = np.random.rand(Np)*blen
posy = np.random.rand(Np)*blen

#Two Lines
#posx = np.random.rand(Np)*blen
#posy[:(Np/2)] = np.ones(Np/2)*(blen/4.0)+(np.random.rand(Np/2)*5-2.5) #np.random.rand(Np)*blen
#posy[(Np/2):] = np.ones(Np/2)*(blen*(3/4.0)) +(np.random.rand(Np/2)*5-2.5)

#Checkerboard 
#posy[:(Np/2)] = np.random.rand(Np/2)*(blen/2.0)
#posx[:(Np/2)] = np.random.rand(Np/2)*(blen/2.0)
#posy[(Np/2):] = blen - posy[:(Np/2)]
#posx[(Np/2):] = blen - posx[:(Np/2)]

#Condens to point
#posx = np.ones(Np)*blen/2
#posy = np.ones(Np)*blen/2


posinterx = np.zeros(Np) #Initializing arrays for interpolation
posintery = np.zeros(Np)

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
    posinterx = np.floor((posx/blen)*(slen-2)-1)
    posintery = np.floor((posy/blen)*(slen-2)-1)

    
def distrho(): #Charge distribution #V slow
    interp()
    rhoacc = np.zeros([slen-2,slen-2])
    
    for i in np.arange(Np):
        rhoacc[posinterx[i],posintery[i]] += q
    
    rhoacc = rhoacc+rho0
    
    rhog[1:(slen-1),1:(slen-1)] = rhoacc

#distrho()
#applyBCmat(rhog)
#draw3(rhog)
        
def computeV(): #I think the math is on point..
    #FFT the charge distribution
    rhocoeff = np.fft.fft2(rhog[1:(slen-1),1:(slen-1)])
    phicoeff = np.zeros([size-2,size-2],'float64')
    
    for i in xrange(slen-2):
        for j in xrange(slen-2):
            phicoeff[i][j] = rhocoeff[i][j]/((i**2+j**2)*np.pi**2)
    phig[1:(slen-1),1:(slen-1)] = np.real(np.fft.ifft2(phicoeff[1:(slen-1),1:(slen-1)]))
    #return phi

#computeV()
#applyBCmat(phig)
#draw3(phig)
        

#up = phigf.reshape(10,10)

def computeE():
    for i in np.arange(1,slen-1):
        for j in np.arange(1,slen-1):
            Ex[i][j] = (phig[i-1][j]-phig[i+1][j])/(2*clen)
            Ey[i][j] = (phig[i][j-1]-phig[i][j+1])/(2*clen)
        
#computeE()
#applyBCmat(Ex)
#applyBCmat(Ey)

#draw3(Ex)     

def computeF():
    culledEx = Ex[1:(slen-1),1:(slen-1)]
    culledEy = Ey[1:(slen-1),1:(slen-1)]
    
    accE = np.sqrt(culledEx**2 + culledEy**2)
    Facc = accE*q
    
    for i in xrange(Np):        
        Fx[i] = Facc[posinterx.astype('int')[i],posintery.astype('int')[i]]*np.cos(Ex[posinterx.astype('int')[i],posintery.astype('int')[i]]/Ey[posinterx.astype('int')[i],posintery.astype('int')[i]])
        Fy[i] = Facc[posinterx.astype('int')[i],posintery.astype('int')[i]]*np.sin(Ex[posinterx.astype('int')[i],posintery.astype('int')[i]]/Ey[posinterx.astype('int')[i],posintery.astype('int')[i]])
        
    #for i in xrange(Np):
    #    Fx[i] = Ex[posinterx.astype('int')[i],posintery.astype('int')[i]]
    #    Fy[i] = Ey[posinterx.astype('int')[i],posintery.astype('int')[i]]

#computeF()
 
def updatevel():
    global vx,vy
    vx = vx + (Fx/m)*DT
    vy = vy + (Fy/m)*DT

#updatevel()
def renorm():
    for i in np.arange(Np):
        if posx[i] > blen:
            posx[i] = posx[i]%blen
        if posy[i] > blen:
            posy[i] = posy[i]%blen
        if posx[i] < 0:
            posx[i] = posx[i]%blen
        if posy[i] < 0:
            posy[i] = posy[i]%blen
        
def updatepos():
    global posx,posy
    posx = posx + vx*DT
    posy = posy + vy*DT
    renorm()

#updatepos())

#Run cycle
#from diagnosticsone import *

def run(cycles):
    for i in np.arange(cycles):
        distrho()
        applyBCmat(rhog)
        computeV()
        applyBCmat(phig)
        computeE()
        applyBCmat(Ex)
        applyBCmat(Ey)
        computeF()
        updatevel()
        updatepos()
        drawtrons()
        draw3(np.transpose(phig))
        #chgcons()
        #if(i%10==0):
        #    drawtrons()
        #draw3(phig)
        print(i,chgcons(),Hcons())
run(iterations)        
        
        
        
#Diagnostic Tools
def draw():
    return test.reshape(slen,slen)
def draw2():
    return np.array(np.arange(0,size)).reshape(slen,slen)
def draw3(mat):
    m = np.matrix(mat.reshape(slen,slen))
    plt.imshow(np.flipud(m),interpolation='nearest',cmap='hot')
    plt.show()
def sumch():
    mat = np.matrix(rhog.reshape(slen,slen))
    return np.sum(mat[1:(slen-1),1:(slen-1)])
def drawtrons():
    #plt.plot(posx,posy,marker='.',linewidth = 0,ms=50,alpha=-0.9)
    plt.plot(posx,posy,marker='x',linewidth = 0)    
    plt.xlim(0,blen)
    plt.ylim(0,blen)
    plt.show()       
def chgcons():
    return np.sum(rhog[1:(slen-1),1:(slen-1)])
def Hcons():
    return np.sum(phig)+np.sum((1/2)*(m)*(vx**2+vy**2)) #Make sure you're computing this right, not cons at all.