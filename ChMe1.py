#THIS DOES NOTT FUCK INGG WORK

import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
rcParams['figure.figsize'] = 13,13


T = 50 # Number of timesteps
BoxLen = 64
dt = 0.5
t = 0



qe = -1.0
me = 1

Ng = 64 #number of gird points
Np = 2  #number of particles
H = 1
Ns = 1 # num sup per part?

x = np.array([15,24])
#x = np.ones(Np)*14
#x[10:] = 26
v = np.zeros(Np)

rho = np.zeros(Ng)
rho0 = 20/64.0
phi = np.zeros(Ng)
E =  np.zeros(Ng)
F =  np.zeros(Np)

def interp(x):
    if np.abs(x) < H/2.0:
        return 1
    else:
        return 0
        

def charge():
    global rho
    rho = np.zeros(Ng)
    selecta = np.zeros(Ng)
    #selecta tells you how much to add to each gp using interp
    for gp in np.arange(Ng):
        selecta[gp] = sum([interp(ex-gp) for ex in x])
    rho += (qe*Ns/H)*selecta + rho0

def field():
    global E
    global phi
    phi = np.zeros(Ng)
    E = np.zeros(Ng)
    
    #phi potential
    for gp in xrange(Ng):
        phi[0] = phi[0] + (gp+1)*rho[gp]
    phi[0] = phi[0]/Ng
    phi[1] = rho[0]+2*phi[0]
    
    for gp in xrange(2,Ng):
        phi[gp] = rho[gp-1] + 2*phi[gp-1] - phi[gp-2]

    #E field
    E[0] = (phi[63] - phi[1])/(2*H)
    E[63] = (phi[62]-phi[0])/(2*H)
    
    for gp in xrange(1,Ng-1):
        E[gp] = (phi[gp-1]-phi[gp+1])/(2*H)
    
def force():
    global F
    F =  np.zeros(Np)
    for i in xrange(Np):
        F[i] = Ns*qe*sum(interp(x[i]-gp)*E[gp] for gp in np.arange(Ng-1))
        
def eom():
    global v
    global x
    #Not leapfrogging this time
    v = v + (F/(Ns*me))*dt
    x = x + v*dt
    for i in xrange(len(x)):
        if(x[i]>64):
            x[i] = x[i] - 64
    
#charge()
#field()
#force()
#eom()
#plt.plot(phi)
#plt.plot(E*10)
#plt.show()
#plt.plot(F)

def run():
    for i in np.arange(0,T,dt):
        charge()
        field()
        force()
        eom()
        plt.plot(np.ones(len(x))*i,x,marker ='x',linewidth=0)
        plt.xlim(0,T)
        plt.ylim(0,64)
        plt.show()
        #plt.plot(E)
        #plt.show()
        print(i)

run()






        