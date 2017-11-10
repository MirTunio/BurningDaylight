# FUN MOD
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
rcParams['figure.figsize'] = 10,10

#Parameters and Setup:
t = 0 #time keeper
dt = 0.05 #time step
tmax = 300 #simulation time
Np = 200 #number of particles, 150 is max that works well

X = random.rand(Np)*15  #Assigning random x values to particles
Y = random.rand(Np)*15 - 7.5 # // y values to particles
Q = np.ones(Np)*0.3 # Assigning charge
Vx = np.zeros(Np) #Creating array for velocities in x 
Vy = np.zeros(Np) #Same for y
M = np.ones(Np)*0.1 #Setting mass of each particle
Fx = np.zeros(Np) #Creating array for forces in x
Fy = np.zeros(Np) #Same for y

M[0] = 1000000
Q[0] = -100
X[0] = -5
Y[0] = 0
    
#Force Law:
def Forcex(i,j,dim): #for x
    #k = 2 #force constant for spring
    rvec = np.array([X[i]-X[j],Y[i]-Y[j]]) #creates vector r
    r = np.sqrt(np.square(rvec[0])+np.square(rvec[1]))
    a = 1.2 #finite radius a of particles
    asq = a**2
    #force = -1*(r)*k #linear force law, springlike
    #k = Q[i]*Q[j] #force constant for coulomb
    if(np.abs(r)>=a): #coulomb force, collisionless
        force = (Q[i]*Q[j])/r*r
    else:
        force = (1/asq)*(8*r*(1/a) - 9*(r**2)*(1/asq) + 2*(r**4)*(1/asq**2))
    return (rvec[0]/r)*force #resolves in x
        
def Forcey(i,j,dim):    #for y
    #k = 2 #force constant for spring
    rvec = np.array([X[i]-X[j],Y[i]-Y[j]]) #creates vector r
    r = np.sqrt(np.square(rvec[0])+np.square(rvec[1]))
    a = 1.2 #finite radius a of particles
    asq = a**2
    #force = -1*(r)*k #linear force law, springlike
    #k = Q[i]*Q[j] #force constant for coulomb
    if(np.abs(r)>=a): #coulomb force, collisionless
        force = (Q[i]*Q[j])/r*r
    else:
        force = (1/asq)*(8*r*(1/a) - 9*(r**2)*(1/asq) + 2*(r**4)*(1/asq**2))
    return (rvec[1]/r)*force #resolves in y
        
#1.Compute forces
def ComputeForces():
    for i in np.arange(Np): #Find force Fij of particle j on particle i
        for j in np.arange(i+1,Np): 
            Fex = Forcex(i,j,'x')
            Fey = Forcey(i,j,'y')
            Fx[i] = Fx[i] + Fex 
            Fx[j] = Fx[j] - Fex 
            Fy[i] = Fy[i] + Fey
            Fy[j] = Fy[j] - Fey
            
#2. Integrate EOM
def EOMintegrate(): # Computes velocites and displacements through numerical integration on timestep dt
    for i in np.arange(Np):
        Vx[i] = Vx[i] + (Fx[i]/M[i])*dt
        X[i] = X[i] + Vx[i]*dt
        Vy[i] = Vy[i] + (Fy[i]/M[i])*dt
        Y[i] = Y[i] + Vy[i]*dt
        
#3. Update Time counter
for i in np.arange(tmax): #updates time, resets arrays, calls required functions
    Fx = np.zeros(Np) #Clear force accumulators
    Fy = np.zeros(Np)
    ComputeForces()
    EOMintegrate()
    t = t + dt
    print(t)
    plt.plot(X,Y,marker = 'x',linewidth = 0,ms=5,color = 'blue')
    plt.plot(X[0],Y[0],marker = '.',linewidth = 0,ms=8,color = 'red')
    plt.xlim(-20,20)
    plt.ylim(-20,20)
    plt.show()
#    plt.plot(X,Y,marker = '.',linewidth = 0,ms=1,color = 'blue')
#plt.ylim(-40,40)
#plt.xlim(-40,40)
#plt.show()
    
    
    
        
        

