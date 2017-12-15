#INCOMPETANT ANTS!

from pylab import rcParams
import numpy as np
rcParams['figure.figsize'] = 9,3
from matplotlib import pyplot as plt

#%% SETUP
BoxX = 1500
BoxY = 800
environment = np.array([[0 for i in range(BoxX)] for j in range(BoxY)])

'''
Environment Codes:
Food: -20
Pheramone trails: +ve number
Home: -10
NoGo: -30
'''

environment[375:425,1000:1050] = -20
environment[375:425,450:500] = -10
environment = np.array(environment)

plt.matshow(environment,cmap='hot',interpolation=None)
plt.show()

#%% ENVIRONMENT HANDLING
decayFactor = 0.0001

def EnvironmentUpdate():
    pheramonesHere =  environment > 0
    environment[pheramonesHere] = environment[pheramonesHere]-decayFactor

environment[375:425,1000:1050] = -20
environment[375:425,450:500] = -10

#%% ANTZ

class ant():
    global environment
    biasX = 0
    biasY = 0

    def __init__(self):
        self.locY = np.random.randint(375,high=426)
        self.locX = np.random.randint(450,high=500)
        self.state = 'EXPLORE'
        self.speed = np.random.randint(25,50)

    def location(self):
        return self.locX,self.locY

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

    def stepHere(self,xx,yy):
        #print(xx,yy)
        if environment[yy,xx] == -20:
            self.state = 'FOODRUN'
        if environment[yy,xx] == -10 and self.state == 'FOODRUN':
            self.state = 'EXPLORE'

    def explore(self):
        self.spreadPheramone(self.locX,self.locY,12)

        self.locX += np.random.randint(-1*self.speed,self.speed)
        self.locX += self.biasX
        self.locX = self.checklocX(self.locX)

        self.locY += np.random.randint(-1*self.speed,self.speed)
        self.locY += self.biasY
        self.locY = self.checklocY(self.locY)

        self.stepHere(self.locX,self.locY)
        self.setBias(self.locX,self.locY)

    def foodRun(self):
        self.spreadPheramone(self.locX,self.locY,24)

        self.locX += np.random.randint(-1*self.speed*0.30,self.speed*0.30)
        self.locX += self.biasX
        self.locX = self.checklocX(self.locX)

        self.locY += np.random.randint(-1*self.speed*0.30,self.speed*0.30)
        self.locY += self.biasY
        self.locY = self.checklocY(self.locY)

        self.stepHere(self.locX,self.locY)
        self.setBias(self.locX,self.locY)

    def spreadPheramone(self,centerX,centerY,amount):
#        kernelX = [self.locX-1, self.locX-1, self.locX-1,
#                   self.locX, self.locX, self.locX,
#                   self.locX+1, self.locX+1, self.locX+1]
#
#        kernelY = [self.locY-1,self.locY,self.locY+1,
#                   self.locY-1,self.locY,self.locY+1,
#                   self.locY-1,self.locY,self.locY+1,]

        kernelX = centerX
        kernelY = centerY
        environment[kernelY,kernelX] += amount

    def setBias(self,xx,yy):
        xscanpos = self.filt(environment[yy,xx:xx+100])
        xscanneg = self.filt(environment[yy,xx-100:xx])
        yscanpos = self.filt(environment[yy:yy+100,xx])
        yscanneg = self.filt(environment[yy-100:yy,xx])

        if xscanpos > xscanneg+30:
            self.biasX = 5
        elif xscanneg > xscanpos+30:
            self.biasX = -5
        else:
            self.biasX = 0

        if yscanpos > yscanneg+30:
            self.biasY = 5
        elif yscanneg > yscanpos+30:
            self.biasY = -5
        else:
            self.biasY = 0

    def filt(self,scan):
        return np.sum([x if x > 0 else 0 for x in scan])

#%% RUN
Time = 30000
Antz = np.array([ant() for i in range(1000)])
splorelog = []

for t in range(Time):
    if t%100 == 0:
        print(t)

    if t%(20) == 0:#and t > 500:
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

        plt.hist2d(anty, antx, bins=50,cmap='hot')
        plt.colorbar()
        plt.show()

        biasx = [antman.biasX for antman in Antz]
        biasy = [antman.biasY for antman in Antz]
        plt.hist2d(biasx, biasy, bins=11,cmap='hot',range = [[-20, 20], [-20, 20]])
        plt.colorbar()
        plt.show()

        print(t)

    [antman.updateLocation() for antman in Antz]
    EnvironmentUpdate()
