#Fresh start
#Reference: Hockney
#Notes:
#The onus is always on the numerical experimenter to demonstrate that the results
#from the simulation model are physically meaningful - we shall see in later chapters
#that numerical errors can have disastrous effects!
#
#A well engineered program should be easy to read, easy to use and easy to modify.
#
#length and timescales of phenomenon in question determine the model, be wise.
#
#We first attempt the PP time step
#
# FIRST SUCCESS!
# tests4 => 2D
#
# Optimized for SPEED
#
# NOWW with LAZERS!
#
# Goals:
# 1000 particles before October
# GPU capability before November
# Full scale simulation befe December
#------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
rcParams['figure.figsize'] = 13,13

#Parameters and Setup:
t = 0 #time keeper
dt = 0.1#05 #time step
tmax = 200 #simulation time
Np = 150 #number of particles, 150 is max that works well

X = random.rand(Np)*25 - 12.5 #Assigning random x values to particles
Y = random.rand(Np)*25 - 12.5 # // y values to particles
Q = np.ones(Np)*-1 #np.random.rand(Np)*2 -1  # Assigning charge
Vx = np.zeros(Np) #Creating array for velocities in x 
Vy = np.zeros(Np) #Same for y
M = np.ones(Np)*0.1 #Setting mass of each particle
Fx = np.zeros(Np) #Creating array for forces in x
Fy = np.zeros(Np) #Same for y

##Outlier for fun:
#M[0] = 1000
#Q[0] = -150


def xnought(t):
    if(t>10):
        M[0] = 1000
        Q[0] = -11
        X[0] = -20 + (t-10)*40
        Y[0] = 0   
        
    else:
        X[0] = -20
        Y[0] = 0
        Q[0] = 0

        
def setlattice(n):
    for i in xrange(1,80):
        M[i] = 50
        Q[i] = 1
        X[i] = -15 + 0.375*i
setlattice(80)     
        
#Force Law:
def Forcex(i,j): #for x
    #k = 2 #force constant for spring
    rvec = np.array([X[i]-X[j],Y[i]-Y[j]]) #creates vector r
    r = np.sqrt(np.square(rvec[0])+np.square(rvec[1]))
    a = 1.2 #finite radius a of particles
    asq = a**2
    #force = -1*(r)*k #linear force law, springlike
    #k = Q[i]*Q[j] #force constant for coulomb
    #if(np.abs(r)>=a): #coulomb force, collisionless
    force = (Q[i]*Q[j])/r*r
    #else:
    #    force = (1/asq)*(8*r*(1/a) - 9*(r**2)*(1/asq) + 2*(r**4)*(1/asq**2))
    return (rvec[0]/r)*force #resolves in x
        
def Forcey(i,j):    #for y
    #k = 2 #force constant for spring
    rvec = np.array([X[i]-X[j],Y[i]-Y[j]]) #creates vector r
    r = np.sqrt(np.square(rvec[0])+np.square(rvec[1]))
    a = 1.2 #finite radius a of particles
    asq = a**2
    #force = -1*(r)*k #linear force law, springlike
    #k = Q[i]*Q[j] #force constant for coulomb
    #if(np.abs(r)>=a): #coulomb force, collisionless
    force = (Q[i]*Q[j])/r*r
    #else:
    #    force = (1/asq)*(8*r*(1/a) - 9*(r**2)*(1/asq) + 2*(r**4)*(1/asq**2))
    return (rvec[1]/r)*force #resolves in y
        
#1.Compute forces
def ComputeForces():
    for i in xrange(Np): #Find force Fij of particle j on particle i
        for j in xrange(i+1,Np): 
            Fex = Forcex(i,j)
            Fey = Forcey(i,j)
            Fx[i] = Fx[i] + Fex 
            Fx[j] = Fx[j] - Fex 
            Fy[i] = Fy[i] + Fey
            Fy[j] = Fy[j] - Fey
    
    
            
#2. Integrate EOM
def EOMintegrate(): # Computes velocites and displacements through numerical integration on timestep dt
    for i in xrange(Np):
        Vx[i] = Vx[i] + np.divide(Fx[i],M[i])*dt
        X[i] = X[i] + Vx[i]*dt
        Vy[i] = Vy[i] + np.divide(Fy[i],M[i])*dt
        Y[i] = Y[i] + Vy[i]*dt
        
#3. Update Time counter
for i in np.arange(tmax): #updates time, resets arrays, calls required functions
    Fx = np.zeros(Np) #Clear force accumulators
    Fy = np.zeros(Np)
    ComputeForces()
    EOMintegrate()
    xnought(t)
    t = t + dt
    print(t)
    if(t>0):
        #plt.plot(X,Y,marker = '.',linewidth = 0,ms=5,color = 'blue',alpha = 10)
        plt.plot(X,Y,marker = '.',linewidth = 0,ms=50,color = 'blue',alpha = 200)
        plt.plot(X[0],Y[0],marker = '.', linewidth = 0, ms = 12, color = 'red')
        for i in np.arange(1,80):
            plt.plot(X[i],Y[i],marker = 'x', linewidth = 0, ms = 8 , color = 'red')
        plt.xlim(-40,40)
        plt.ylim(-40,40)
        plt.show()
#    plt.plot(X,Y,marker = '.',linewidth = 0,ms=1,color = 'blue')
#plt.ylim(-40,40)
#plt.xlim(-40,40)
#plt.show()
    
    
    
        
        

