import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
rcParams['figure.figsize'] = 13,13

#Parameters:
# x goes from 0 to 300
# will be bins of width 10, so 30 cells / 3 superparticles (rite)?
#

L = 100.0 # lenght of region
Np = 200 # No of e-
x = np.random.rand(Np)*L
q = -1

rho_0 = (q*-1)*Np/L  #bg density of charge
H = 5 # width of cell
Ns = 40 # so each sp rep 5 particles
Nc = ((rho_0*H)/(Ns*np.abs(q))) #Avg number of sup.particle per cell
Ng = int(L/H)

Wp = 0.5 #something
DT = 0.5 #delta time
T = 50 #total timesteps
def NGP(pos):
    return np.round(pos/10.0)
    
        #tests for NGP:
        #plt.hist([NGP(c) for c in x],bins = 30,color='black',alpha=0.5) 
        #plt.plot(x/10,np.zeros(Np)+5,linewidth = 0, marker = 'o',alpha = 0.08)


#1. Distribute charge:
    #1.1 Initialize charge density accumulators:
rho = np.ones(Ng)*-1*Nc

    #1.2 Accumulate charge density:
pnew = np.round((x-0.2)/5.2).astype(int) # effectively applies NGP 
for p in pnew:
    rho[p] = rho[p]+1

    #1.3 Scale charge densities:
for p in xrange(Ng):
    rho[p] = (Wp**2)*(DT**2)*rho[p]/(2*Nc)

        #tests for charge dist:
        #plt.plot(rho,linewidth = 0,marker='x')
        #plt.show()
        #plt.plot(x,linewidth = 0,marker='x')
        #plt.show()
        #plt.plot(pnew,linewidth = 0,marker='x')
        #plt.show()

#2. Field Equations:
    phi = np.zeros(Ng)
    
    # Potential at mesh point 0
    for p in xrange(1,Ng):
        phi[0]  = phi[0] + p*rho[p]
    phi[0] = phi[0]/Ng
    
    # Potential at mesh point 1
    phi[1] = rho[0]+2*phi[0]
    
    # Remaining potentials
    for p in xrange(2,Ng):
        phi[p] = rho[p-1] + 2*phi[p-1]-phi[p-2]
    

#CLEARLY, something is fucked up.
#Lets see if there is some better example code.
