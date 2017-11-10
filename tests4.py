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


#------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
rcParams['figure.figsize'] = 6,4

#Parameters:
t = 0
dt = 0.05
tmax = 200
Np = 50
X = random.rand(Np)*10 - 5 #Assigns random position between -5 and 5
Y = random.rand(Np)*10 - 5# // 
Q = random.rand(Np)*2 - 1
Vx = np.zeros(Np)
Vy = np.zeros(Np)

M = np.ones(Np)*2
Fx = np.zeros(Np)
Fy = np.zeros(Np)

#Outlier for fun:
#M[5] = 100
#X[5] = -10
#Y[5] = -10

#Force Law:
def Force(i,j,dim):    
    k = 2
    if(dim=='x'):
        r = X[i]-X[j]
    else:
        r = Y[i]-Y[j]
        
    a = 1.2
    #force = -1*(r)*k #linear force law, springlike
    k = Q[i]*Q[j]
    if(np.abs(r)>=a):# coulomb
        force = -1*k/r*r
    else:
        force = -1*(1/a**2)*(8*r*(1/a) - 9*(r**2)*(1/a**2) + 2*(r**4)*(1/a**4))
    return force
    
#1.Compute forces
def ComputeForces():
    for i in np.arange(Np-1): #Find force Fij of particle j on particle i
        for j in np.arange(i+1,Np):
            Fx[i] = Fx[i] + Force(i,j,'x')+10*random.normal() #+ Force(Y[i],Y[j])
            Fx[j] = Fx[j] - Force(i,j,'x')+10*random.normal() #- Force(Y[i],Y[j])
            Fy[i] = Fy[i] + Force(i,j,'y')+10*random.normal() #+ Force(X[i],X[j])
            Fy[j] = Fy[j] - Force(i,j,'y')+10*random.normal() #- Force(Y[i],Y[j])
            
#2. Integrate EOM
def EOMintegrate():
    for i in np.arange(Np):
        Vx[i] = Vx[i] + (Fx[i]/M[i])*dt
        X[i] = X[i] + Vx[i]*dt
        Vy[i] = Vy[i] + (Fy[i]/M[i])*dt
        Y[i] = Y[i] + Vy[i]*dt
        
#3. Update Time counter
for i in np.arange(tmax):
    Fx = np.zeros(Np) #Clear force accumulators
    Fy = np.zeros(Np)
    ComputeForces()
    EOMintegrate()
    t = t + dt
    print(t)
    plt.plot(X,Y,marker = 'x',linewidth = 0,ms=6)
    plt.xlim(-20,20)
    plt.ylim(-20,20)
    plt.show()
    
    
    
        
        

