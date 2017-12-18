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


#------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
rcParams['figure.figsize'] = 6,4

#Parameters:
t = 0
dt = 0.1
Np = 10
X = random.rand(Np)*10 #Assigns random position between 0 and 10
V = np.zeros(Np)
M = np.ones(Np)*2
F = np.zeros(Np)

#Force Law:
def Force(a,b):    
    k = 2
    force = -1*(X[a]-X[b])*k #linear force law, springlike
    return force
    
#1.Compute forces
def ComputeForces():
    for i in np.arange(Np-1): #Find force Fij of particle j on particle i
        for j in np.arange(i+1,Np):
            F[i] = F[i] + Force(i,j)
            F[j] = F[j] - Force(i,j)

#2. Integrate EOM
def EOMintegrate():
    for i in np.arange(Np):
        V[i] = V[i] + (F[i]/M[i])*dt
        X[i] = X[i] + V[i]*dt
        
#3. Update Time counter
for i in np.arange(400):
    F = np.zeros(Np) #Clear force accumulators
    ComputeForces()
    EOMintegrate()
    t = t + dt
    print(t)
    plt.plot(X,np.zeros(Np),marker = 'x',linewidth = 0)
    plt.xlim(0,10)
    plt.show()
    
    
    
        
        

