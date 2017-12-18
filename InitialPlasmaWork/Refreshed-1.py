#Lets do this one more time, periodic boundary conditions, just plain poisson
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
from scipy import ndimage

rcParams['figure.figsize'] = 13,13

#Parametesr
slen = 10
size = slen**2
test = np.array(np.arange(0,size),dtype='float64')
DT = 0.2

#Setting Corners of grid
test[0] = 0
test[slen-1] = 0
test[size - slen] = 0
test[size-1] = 0

def applyBC():
    #setting top and bottom
    test[1:slen-1] = test[size - 2*slen+1:size - slen -1]
    test[size - slen + 1:size-1] = test[slen+1:2*slen-1]
    #setting sides
    for i in np.arange(1,slen-1):
        test[slen*i] = test[slen*(i+1)-2]
    
    for i in np.arange(1,slen-1):
        test[slen*(i+1)-1] = test[slen*i+1]
    
    mat = np.matrix(test.reshape(slen,slen))
    plt.imshow(mat,interpolation='nearest')

#set charges:
def setcharges():
    global test
    insum = 0
    tsum = 0
    #assigning random negative charges
    for i in np.arange(1,slen-1):
        setc = -1*np.random.rand(slen-2)*10
        test[slen*i+1:slen*(i+1)-1] = setc
        insum += sum(setc)
        #print(sum(setc),insum)
    rho0 = -1*insum/((slen-2)**2)
    #print(rho0)
    
    #applying background accordingly to conserve
    for i in np.arange(1,slen-1):
       test[slen*i+1:slen*(i+1)-1] =  test[slen*i+1:slen*(i+1)-1] + rho0*np.ones(slen-2)
       tsum += sum(test[slen*i+1:slen*(i+1)-1])
       #print(sum(test[slen*i+1:slen*(i+1)-1]))
    print(tsum)
    
       
def draw():
    return test.reshape(slen,slen)
def draw2():
    return np.array(np.arange(0,size)).reshape(slen,slen)
def draw3():
    mat = np.matrix(test.reshape(slen,slen))
    plt.imshow(mat,interpolation='nearest')
    
initialize()
    
    
def initialize():
    setcharges()
    applyBC()
    draw3()
    return draw()
    
#initialize
#compute potentials
def computeV():
    k = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
    testpot = ndimage.convolve(test.reshape(slen,slen), k, mode='constant', cval=0.0)

def draw4():
    mat = np.matrix(testpot)
    plt.imshow(mat,interpolation='nearest')

#compute field
kx = np.array([[0,0,0],[1,0,-1],[0,0,0]])
ky = np.array([[0,1,0],[0,0,0],[0,-1,0]])

testEx = ndimage.convolve(testpot, kx, mode='constant', cval=0.0)
testEy = ndimage.convolve(testpot, ky, mode='constant', cval=0.0)

def draw5():
    mat = np.matrix(testE)
    plt.imshow(mat,interpolation='nearest')

#setting v vals

 