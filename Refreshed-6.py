#Writing it again, fixing bugs, making more professional
#EDGE CASES
    
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from collections import Counter
rcParams['figure.figsize'] = 6,6

#Parameters
#Arena
blen = 200.0 #size of box
glen = 5#21   #set number grid points along length of box
Ng = glen**2 #number of grid points
clen = blen/glen # size of the cell
Np = 10 #number of particles

#Other
iterations = 600 #number of cucles
DT = 1 #time step per cycle
q = -1 #charge of superpartiles
m = 0.1 #mass of particles

#Initializing Arrays
#charge
#rhog = np.array(np.arange(0,size),dtype='float64') #the grid #diagnostic version
rhog = np.zeros([glen,glen],dtype='float64') #the grid for rho
rho0 = -1*(Np*q)/float(Ng)

#Potential
#phig = np.array(np.arange(0,size),dtype='float64').reshape(slen,slen)
phig = np.zeros([glen,glen],dtype='float64')

#Electric Field
Ex = np.zeros([glen,glen])
Ey =  np.zeros([glen,glen])

#Position
#Random positioning
posx = np.random.rand(Np)*blen
posy = np.random.rand(Np)*blen

#Force
Fx = np.zeros(Np,dtype='float64')
Fy = np.zeros(Np,dtype='float64')

#Velocities
vx = np.zeros(Np)
vy = np.zeros(Np)

def interp(obj): #interpolation scheme, object defined in box length parameters
    return np.round((obj/blen)*(glen-1)).astype('int')
    
def distrho(): #Charge distribution over rhog
    global rhog
    posinterx = interp(posx)
    posintery = interp(posy)
    rhoacc = np.zeros([glen,glen])
    
    for i in np.arange(Np):
        rhoacc[posinterx[i],posintery[i]] += q
    
    rhoacc = rhoacc+rho0
    rhog = rhoacc

def computeV(): #Computes potential with FFT, over phif
    global phig
    rhocoeff = np.fft.fft2(rhog) #FFT of rho
    phicoeff = np.zeros([glen,glen],'float64')
    
    for i in xrange(glen):
        for j in xrange(glen):
            phicoeff[i][j] = rhocoeff[i][j]/((i**2+j**2)*np.pi**2)
    print(phicoeff) 
    phig = np.real(np.fft.ifft2(phicoeff)) #DC the math

def computeE():
    for i in np.arange(-1,glen-1):
        for j in np.arange(-1,glen-1):
            Ex[i][j] = (phig[i-1][j]-phig[i+1][j])/(2*clen)
            Ey[i][j] = (phig[i][j-1]-phig[i][j+1])/(2*clen)

    
distrho()
computeV()
computeE()