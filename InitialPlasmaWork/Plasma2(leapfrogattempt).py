# -*- coding: utf-8 -*-
"""
Author: Murtaza Tunio
Title: Attempt to create 1D leapfrog simulation for plasma physics purposes
"""
#NOTES:
#LOL, same timing, half codespeed. Useless crap.

import numpy as np
import matplotlib.pyplot as plt
import time


ForceConstant = 1.0
pipe = np.arange(0.1,10,0.1)
Eplot = np.array([])
Splot = np.array([])

accl = np.array([])
vell = np.array([])
posl = np.array([])
EForcel = np.array([])
SForcel = np.array([])
timel = np.array([])
tick = 0

def EForce(x):
    return -10.0*ForceConstant/x**2
def SForce(x):
    return 100.0*(ForceConstant)/x**4
    
pos = 10.0
vel = 0.0
mass = 2.0
runlen = 200.0
deltime = 1
acc = 0.0

def update():
    global vel
    global pos
    global tick
    
    if tick%2 == 0:
        vel = vel + acc*deltime
    else:
        pos = pos + vel*deltime
    tick+=1

for i in np.arange(0,runlen,deltime):
    startime = time.time()
    print(acc)
    print(vel)
    print(pos)
    accl = np.append(accl,acc)
    vell = np.append(vell,vel)
    posl = np.append(posl,pos)
    
    EForcel = np.append(EForcel,EForce(pos))
    SForcel = np.append(SForcel,SForce(pos))
    
    plt.plot(pos,0,marker = 'o',ms=10)
    acc = (EForce(pos)+SForce(pos))/mass
    update()
    
    plt.xlim(-100,100)
    plt.plot(0,0,marker='x',ms=20,c='black')
    plt.show()
    endtime = time.time()
    runlen = endtime-startime
    print(runlen)
    timel = np.append(timel,runlen)
    
plt.plot(accl)
plt.show()
plt.plot(vell)
plt.show()
plt.plot(posl)
plt.show()


for i in pipe:
    Eplot = np.append(Eplot,EForce(i))
    Splot = np.append(Splot,SForce(i))
    plt.xlim(0,100)
    plt.plot(Eplot+Splot)



#class particle2:
#    def __init__(self,pos_i,vel_i):
#        self.pos = pos_i
#        self.vel = vel_i
#    
#particlelist = ?
#    
#
#def leapfrog(plist):
#    for particle in plist:
#        updatepos(particle)
#        updatevel(particle)
#
#def step(n):
#    for i in xrange(n):
#        print(n)
#        leapfrog(particlelist)
#        display(particlelist)
#        
#def display(plist):
#    for particle in plist:
#        plt.plot(particle.pos,marker='o',c='b',ms=10)
#    
#def updatevel(part):
#    
#def updatepos(part):
    