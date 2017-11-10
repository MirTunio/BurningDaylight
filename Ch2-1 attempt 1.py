import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
from numpy import random
rcParams['figure.figsize'] = 13,13

# Continuing from notes:
#
# Beginning with effeicient charge dist. method:
#
rho_nought = 200;
H = 10
Ns = 100
q = -1
Ng = 10
Npp = 300
Nc = rho_nought*H/(Ns*np.abs(q))
wp = 2
D = 0.5

rho = np.zeros(Npp)
x = np.random.rand(Npp)*300
#1.
for p in np.arange(Ng):
    rho[p] = -Nc

#2.
def nint(x):
    return np.round(x/10.0)
    
for j in np.arange(Npp):
    ngp = nint(x[j])
    rho[ngp] = rho[ngp] + 1

#3.
for p in np.arange(Ng):
    rhon = ((wp**2)*D**2/(2*Nc))*rho[p]

plt.plot(x,rho, linewidth= 0, marker = 'x')
