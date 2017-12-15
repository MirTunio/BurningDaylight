#INCOMPETANT ANTS!

from pylab import rcParams
import numpy as np
rcParams['figure.figsize'] = 9,3
from matplotlib import pyplot as plt

#%% SETUP
BoxX = 1500
BoxY = 1500
environment = np.array([[0 for i in range(BoxX)] for j in range(BoxY)])

'''
Environment Codes:
Food: -20
Pheramone trails: +ve number
Home: -10
NoGo: -30
'''

environment = np.array(environment)

plt.matshow(environment,cmap='hot',interpolation=None)
plt.show()

#%% ENVIRONMENT HANDLING
decayFactor = 0.001
def EnvironmentUpdate():
    pheramonesHere =  environment > 0
    environment[pheramonesHere] = environment[pheramonesHere]-decayFactor

#%% ANTZ

class ant():
    global environment
    biasX = 0
    pheramoneFUEL = 1500

    def __init__(self):
        self.locY = np.random.randint(1,high=20)
        self.locX = np.random.randint(750,high=850)
        self.state = 'EXPLORE'
        self.speed = np.random.randint(25,50)

    def updateLocation(self):
        if self.state == 'EXPLORE':
            self.explore()
        elif self.state == 'FOODRUN':
            self.foodRun()
        else:
            raise ValueError('State invalid: %c' % self.state)

    def checklocX(self,xpos):
        if xpos <= 0:
            #print('1',xpos)
            xpos =  BoxX + xpos - 1
        if xpos >= BoxX:
            #print('2',xpos)
            xpos =  xpos - BoxX
        #print('3',xpos)
        return xpos

    def checklocY(self,ypos):
        if ypos <= 0:
            #print('A',ypos)
            ypos =  BoxY + ypos - 1
        if ypos >= BoxY:
            #print('B',ypos)
            ypos =  ypos - BoxY
        #print('C',ypos)
        return ypos

    def explore(self):
        self.setBias(self.locX,self.locY)

        self.locX += np.random.randint(-1*self.speed,self.speed)
        self.locX += self.biasX
        self.locX = self.checklocX(self.locX)

        self.locY += np.random.randint(-10,self.speed)
        self.locY += self.biasY
        self.locY = self.checklocY(self.locY)

        self.spreadPheramone(self.locX,self.locY,16)
        self.pheramoneFUEL += environment[self.locY,self.locX]


    def spreadPheramone(self,centerX,centerY,amount):
        kernelX = centerX
        kernelY = centerY

        if (self.pheramoneFUEL - amount) > 0:
            environment[kernelY,kernelX] += amount
            self.pheramoneFUEL -= amount
        else:
            environment[kernelY,kernelX] += 5
            self.pheramoneFUEL -= 5


    def setBias(self,xx,yy):
        xscanpos = environment[yy,xx:xx+100]
        xscanneg = environment[yy,xx-100:xx]
        yscanpos = environment[yy:yy+100,xx]
        yscanneg = environment[yy-100:yy,xx]

        xscanpos = np.sum(xscanpos[xscanpos>0])
        xscanneg = np.sum(xscanneg[xscanneg>0])
        yscanpos = np.sum(yscanpos[yscanpos>0])
        yscanneg = np.sum(yscanneg[yscanneg>0])

        self.biasX = 20*(xscanpos-xscanneg)/(xscanpos+xscanneg) - 5
        self.biasY = 5*(yscanpos-yscanneg)/(yscanpos+yscanneg)

#%% RUN
Time = 120000000
Antz = np.array([ant() for i in range(500)])
splorelog = []

for t in range(Time):
    if t%100 == 0:
        print(t)

    if t%(25) == 0:#and t > 500:
        environmentoverlay = environment.copy()
        antx = [antman.locX for antman in Antz]
        anty = [antman.locY for antman in Antz]


#        ok = environmentoverlay != 0.0
#        environmentoverlay[ok] = 1

        environmentoverlay[anty,antx] = 2

        explorenum = np.count_nonzero([antman.state == 'EXPLORE' for antman in Antz])
        splorelog.append(explorenum)

        plt.matshow(environmentoverlay,cmap='hot',vmin=-2,vmax=10)
        plt.title('Exploring Now: ' + str(explorenum))
        plt.show()
#
#        plt.hist2d(anty, antx, bins=50,cmap='hot')
#        plt.colorbar()
#        plt.show()
#
#        biasx = [antman.biasX for antman in Antz]
#        biasy = [antman.biasY for antman in Antz]
#        plt.hist2d(biasx, biasy, bins=11,cmap='hot',range = [[-20, 20], [-20, 20]])
#        plt.colorbar()
#        plt.show()

        print(t)

    [antman.updateLocation() for antman in Antz]
    EnvironmentUpdate()
