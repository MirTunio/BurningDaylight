#tests1.py
#Experimenting with plasma sims
#1D electrostatic PIC model
#ref: scan1.pdf

import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 6,4

#1D Electrostatic Simulation
#Maxwell equation resolves to Poisson equation
#(del)^2*phi = -sigma
#D^2(phi)= -S
#OKAY

#For PIC model, need charge density on the discrete spatial grid
#from the coninuous particle position

#Use NGP (Nearest Grid Point), and Linear interp. (CIC,PIC)
#Point charge at x_i, grid point x_j, assign of charge dens S_j
#S_j(x_i) = q*max[0,1-|x_j-x_i|/dx]
#

dx = 1

#Function returns assignment of charge density of a point particle
#of charge q at location x_i (continuous) to a grid point x_j (on grid)
#(Perhaps this is how get around singularities, 'Short range collisions eliminated')
def s_j(x_i,x_j,q):
    return q*np.max([0,1-np.abs(x_j-x_i)/dx])
    
#Plotting S_j    
space = np.arange(-10,11) #GRID
x_i_loc = 1.3
s_j_plot = [s_j(x_i_loc,pointinspace,1) for pointinspace in space]
plt.plot(space,s_j_plot)
plt.show()

#Moving to n-particle framework:
xlocs = np.array([1.4,2.3,3.8,2.1,2.8,7.2])
xqs =  np.array([1,1,1,1,1,1])


#makes computation for given space. for point, call eacj s_
def compforspace(xlocs,xqs, space):
    s_j_plot_glob = np.zeros(len(space))
    for i in np.arange(len(xlocs)):
        #print(s_j_plot_glob)
        s_j_plot_glob = s_j_plot_glob + [s_j(xlocs[i],pointinspace,xqs[i]) for pointinspace in space]
    return s_j_plot_glob
   
s_j_plot_glob = compforspace(xlocs,xqs,space)

#Plotting s_j for that   
#NOTE: s_j_plot_glob represents charge density on the grid
plt.plot(space,s_j_plot_glob)
plt.plot(xlocs,np.ones(len(xlocs))*0.1,marker = 'x',ms=15,linewidth=0)
plt.xlabel('Grid Points')
plt.ylabel('Charge Density (arb)')
plt.grid()
plt.show()

#Electric field on particle at x_i:
#so as in text, S(x_j-x_i)= max[0,1-|x_j-x_i|/dx]
#This is the same as s_j defined above, with q = 1, so:
#Same convolution scheme for E field:
#E_i(x_i) = integral(dx*ShapeF(x-x_i)*E_j(x))

#Defining shape function:
def ShapeF(x_i,x_j):
    return s_j(x_i,x_j,1)


#Plot of shape function:
testspace = np.arange(-20,21)
ShapeF_plot = compforspace(xlocs,xqs,testspace)
plt.plot(testspace,ShapeF_plot)
plt.ylabel('Shape Function')
plt.xlabel('Grid Points')
plt.show()

#del dot E = sigma









