'''
DTW
'''
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 12,4

#%%
#time = np.arange(0,3*np.pi+0.001,np.pi/2)
#signal = [np.sin(t) for t in time]
#signalW = signal + (np.random.random(len(time))-0.5)
#
#timeW = np.dot(time,np.identity(len(time))*(0.5+np.random.random())+0.015)
##%%
time = np.arange(0,2*np.pi,0.1)
signal = [np.cos(t) for t in time]

timeW = time
signalW = [np.sin(t+np.pi/3) for t in timeW]

#%%
D = [[0 for x in np.arange(len(time))] for y in np.arange(len(time))]
for i in np.arange(len(time)):
    for j in np.arange(len(timeW)):
        D[i][j] = np.sqrt((time[i]-timeW[j])**2 + (signal[i]-signalW[j])**2)
        
#%%
fig, (ax1,ax2,ax3) = plt.subplots(nrows=1, ncols=3)

ax1.plot(time,signal,label='Signal',linewidth=2,alpha=0.8,marker='x')
ax1.plot(timeW,signalW,label='SignalA',linewidth=2,alpha=0.8,marker='x')
plt.legend()

mat = ax2.matshow(D,label='D')
fig.colorbar(mat,cax=ax3)

plt.show()

#%%
def WTW(Dprime):
    #plt.matshow(Dprime)
    #print(np.array(Dprime).round(2))
    try:
        right = Dprime[1][0]
    except:
        right = np.inf
    try:
        down =  Dprime[0][1]
    except:
        down = np.inf
    try:
        diag =  Dprime[1][1]
    except:
        diag = np.inf
    
    if (right<down) and (right<diag):
        #print(right,down,diag)
        #print('right')
        return 1,0
    elif (down<diag):
        #print(right,down,diag)
        #print('down')
        return 0,1
    else:
        #print(right,down,diag)
        #print('diag')
        return 1,1
    

def POLR(D):
    D = np.array(D)
    pathlogx = []
    pathlogy = []
    
    pathlogx.append(0)
    pathlogy.append(0)
        
        
    while ((pathlogx[-1] != len(D)-1) and (pathlogy != len(D)-1)): #not((pathlogx[-1] == len(D)-1) or (pathlogy[-1] == len(D)-1)):
        
        l =  pathlogy[-1]
        s =  pathlogx[-1]
            
        ex,ey = WTW(D[s:,l:])
            
        pathlogx.append(ex+s)
        pathlogy.append(ey+l)
        
        #print(pathlogx)
        #print(pathlogy)
        #print('')
        
        
    return pathlogx,pathlogy 

x = np.array(POLR(D))

print(np.array(x))  

rcParams['figure.figsize'] = 8,8
plt.plot(x[0],x[1])
plt.show()

#%%
plt.plot(time,signal,label='Signal',linewidth=2.5,alpha=0.8,c='red')
plt.plot(timeW,signalW,label='SignalA',linewidth=2.5,alpha=0.8,c='purple')


twdist = 0

for M in x.T:
    global twdist
    
    Mx = M[0]
    My = M[1]
    
    plt.plot([time[Mx],timeW[My]],[signal[Mx],signalW[My]],alpha=0.3,linewidth=2,c='black')
    
    twdist += D[Mx][My]
#    time
#    timeW
#    
#    signal
#    signalW
#    
#    plt.plot([a,A],[s,S],alpha=0.1,c='blue')
plt.show()
print('done')
    
#%%
mdist = np.sum(np.array(signal) - np.array(signalW))

print(mdist,twdist)
    