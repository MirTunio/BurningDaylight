# CH STRAIGHT UP COPY
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
rcParams['figure.figsize'] = 13,13
#-------------------------------------------

NRUN = 50 # Number of timesteps
DT = 0.5
T = 0

#Various Constants
pi = 3.14159265
kb = 1.0
qe = -1.0
me = 1
ep = 1

boxlen = 64.0
bgdens = 1.0
initT = 1.0
vdrift = 0.0

xmin = 2.0
x = np.array([10.0, 26.0])
v2pt2 = 0.0

tst1 = 0.01 #temp stream 1
tst2 = 0.01 #temp stream 2
vdr1 = 1.0  #drift vel stream 1
vdr2 = -1.0 #drift vel stream 2
nst1 = 1000 #num part stream 1
nst2 = 1000 #num part stream 2

Ng = 64 #number of gird points
NP = 2  #number of particles

Nc = bgdens/2

FRPDT = 0.25 #plasma freq into time step
#--------------------------------------------
rho = np.ones(Ng)*-1*Nc
phi = np.zeros(Ng)
E = np.zeros(Ng)
F = np.zeros(len(x))
v = np.zeros(len(x))
#--------------------------------------------

def NGP(pos):
    return np.round(pos/64.0)
    
        #tests for NGP:
        #plt.hist([NGP(c) for c in x],bins = 30,color='black',alpha=0.5) 
        #plt.plot(x/10,np.zeros(Np)+5,linewidth = 0, marker = 'o',alpha = 0.08)

#1. Distribute charge:
    #1.1 Initialize charge density accumulators:


def charge():
        #1.2 Accumulate charge density:
    pnew = np.round((x-0.2)/5.2).astype(int) # effectively applies NGP 
    for p in pnew:
        rho[p] = rho[p]+1
    
        #1.3 Scale charge densities:
    for p in xrange(Ng):
        rho[p] = (FRPDT**2)*rho[p]/(2*Nc)
    
            #tests for charge dist:
            #plt.plot(rho,linewidth = 0,marker='x')
            #plt.show()
            #plt.plot(x,linewidth = 0,marker='x')
            #plt.show()
            #plt.plot(pnew,linewidth = 0,marker='x')
            #plt.show()

#2 Compute Fields:

        #2.1 Compute potential at mesh point 0, Solve Poisson
def fields():
    for p in xrange(Ng):
        phi[0] = phi[0] + p*rho[p]
    phi[0] = phi[0]/Ng
    phi[1] = rho[0] + 2*phi[0]
    
    for p in xrange(2,Ng):
        phi[p] = rho[p-1] + 2*phi[p-1] - phi[p-2] # GOING WITH THIS, IS STRANGE
        
        #2.2
    for p in xrange(1,Ng-1):
        E[p] = (phi[p-1] - phi[p+1])/(2*1)
    
#3 Force Interp:
g = np.arange(0,boxlen,1)
def force():
    def Winter(ex):
        if(np.abs(ex)<0.5):
            return 1
        else:
            return 0
            
    for i in xrange(len(x)):
        fsum = 0
        for p in xrange(Ng-1):
            fsum += Winter(x[i] - g[p])*E[p]
        F[i] = 2*qe*fsum


    
def EOM():
    for i in xrange(len(x)):
        v[i] = v[i] + (F[i]/(NP*me))*DT
        x[i] = x[i] + v[i]*DT
        
def run():
    global T
    charge()
    fields()
    force()
    EOM()
    showme()
    #print(x,v,F)
    if(T<NRUN):
        T+=DT

def showme():
    #plt.plot([T,T],x,linewidth = 0, marker ='x',color='black')
    #plt.xlim([0,NRUN])
    #plt.ylim([0,64])
    plt.show()

for i in np.arange(100):
    plt.plot(phi)
    plt.show()
    print(T)
    run()



