# INCOMPETANT ANTS!

# It is time to rethink how you made these ants work
# It should naturally converge to the optimal
# And it is strange that you have had to try so hard
# To help it ...


#Ants should go one step at at time
#Should be released at regular intervals
#I want to see a pheramone trail!

from pylab import rcParams
import numpy as np
rcParams['figure.figsize'] = 5,5
from matplotlib import pyplot as plt
from noise import pnoise1

#%% TERRAIN SETUP

BoxX = 200
BoxY = 200
environment = np.array([[0. for i in range(BoxX)] for j in range(BoxY)])

'''
Environment Codes:
Food: -20
Pheramone trails: +ve number
Home: -10
NoGo: -30
'''

environment[5:15,95:106] = 1000
environment[150:160,95:106] = 1000
#environment[80:90,71:81] = 1000
plt.matshow(environment,cmap='hot',interpolation=None)
plt.show()

decayFactor = 0.025

def EnvironmentUpdate():
    pheramonesHere =  environment > 0
    environment[pheramonesHere] = environment[pheramonesHere] - decayFactor
    environment[5:15,95:106] = 1000
    environment[150:160,95:106] = 1000
#    environment[80:90,71:81] = 1000

environmentmap = np.array([[0. for i in range(BoxX)] for j in range(BoxY)])
environmentmap[5:5,95:106] = -10
environmentmap[150:160,95:106] = -20
#environmentmap[95:106,71:81] = -20

#%% ANT
#x = []
#for i in np.arange(0,100,0.0001):
#    x.append(pnoise1(i,2))
#plt.plot(x)
#plt.show()

class ant():
    global environment
    global environmentmap

    def __init__(self):
        self.biasX = 0
        self.biasY = 0
        self.locY = np.random.randint(5,high=16)
        self.locX = np.random.randint(95,high=106)
        self.state = 'EXPLORE'

    def updateLocation(self):
        if self.state == 'EXPLORE':
            self.explore()
        elif self.state == 'FOODRUN':
            self.foodRun()
        elif self.state == 'DEAD':
            self.dead()

    def checklocX(self,xpos):
        if xpos <= 0:
            self.state = 'DEAD'
            return 1
        if xpos >= BoxX-1:
            self.state = 'DEAD'
            return BoxX-2
        return xpos

    def checklocY(self,ypos):
        if ypos <= 0:
            self.state = 'DEAD'
            return 1
        if ypos >= BoxY-1:
            self.state = 'DEAD'
            return BoxY-2
        return ypos

    def stepHere(self,xx,yy):
        xx = int(np.floor(xx))
        yy = int(np.floor(yy))

        if self.state == 'EXPLORE' and environmentmap[yy,xx] == -20:
            self.state = 'FOODRUN'

        if self.state == 'FOODRUN' and environmentmap[yy,xx] == -10:
            self.state = 'EXPLORE'

    def dead(self):
        self.locY = np.random.randint(5,high=15)
        self.locX = np.random.randint(95,high=106)
        self.state = 'EXPLORE'

    def explore(self):
        self.spreadPheramone(self.locX,self.locY,.5)
        self.locX += np.random.randint(-5,6) + self.biasX #+ np.random.randint(5)
        self.locX = self.checklocX(self.locX)
        self.locY += np.random.randint(-5,6) + self.biasY + np.random.randint(5)
        self.locY = self.checklocY(self.locY)
        self.stepHere(self.locX,self.locY)
        self.setBias(self.locX,self.locY)

    def foodRun(self):
        self.spreadPheramone(self.locX,self.locY,4.)
        self.locX += np.random.randint(-5,6) + self.biasX #- np.random.randint(5)
        self.locX = self.checklocX(self.locX)
        self.locY += np.random.randint(-5,6) + self.biasY - np.random.randint(5)
        self.locY = self.checklocY(self.locY)
        self.stepHere(self.locX,self.locY)
        self.setBias(self.locX,self.locY)

    def spreadPheramone(self,xx,yy,amount):
        xx = int(np.floor(xx))
        yy = int(np.floor(yy))
        environment[yy,xx] += amount

    def setBias(self,xx,yy):
        xscanpos = environment[yy,xx:xx+25]
        xscanneg = environment[yy,xx-25:xx]
        yscanpos = environment[yy:yy+25,xx]
        yscanneg = environment[yy-25:yy,xx]

        xscanpos = np.sum(xscanpos[xscanpos>0])
        xscanneg = np.sum(xscanneg[xscanneg>0])
        yscanpos = np.sum(yscanpos[yscanpos>0])
        yscanneg = np.sum(yscanneg[yscanneg>0])

        if xscanpos > xscanneg:
            self.biasX = np.random.randint(3)
        elif xscanneg > xscanpos:
            self.biasX = -1*np.random.randint(3)
        else:
            self.biasX = 0

        if yscanpos > yscanneg:
            self.biasY = np.random.randint(3)
        elif yscanneg > yscanpos:
            self.biasY = -1*np.random.randint(3)
        else:
            self.biasY = 0

#%% RUN
Time = 500
Antz = [ant() for i in range(10)]
splorelog = []

#%%
for t in range(Time):
    if t%30 == 0:
        Antz.append(ant())
        Antz.append(ant())
        Antz.append(ant())
        Antz.append(ant())
        Antz.append(ant())
        Antz.append(ant())
#        print('New Ants!')

    if t%(10) == 0: #0:# 10
        environmentoverlay = environment.copy()
        antx = [antman.locX for antman in Antz]
        anty = [antman.locY for antman in Antz]

#        ok = environmentoverlay != 0.0
#        environmentoverlay[ok] = 1

        environmentoverlay[anty,antx] = 2

        explorenum = np.count_nonzero([antman.state == 'EXPLORE' for antman in Antz])
        allnum = len(Antz)
        #pheramonenum = np.count_nonzero(environment>0)
        splorelog.append(explorenum)

        plt.matshow(environmentoverlay,cmap='plasma',vmin=-5,vmax=10)#400)#3000)
        plt.colorbar()
        plt.title('Exploring Now: ' + str(explorenum) + ' of ' + str(allnum))# + ' ' + str(pheramonenum))
        plt.savefig('C'+str(t)+'.png')
#        plt.clf()
#        plt.cla()
        plt.show()

#        plt.hist2d(anty, antx, bins=50,cmap='hot',range = [[0, 200], [0, 200]],vmin=0,vmax=5)
#        plt.show()
#
#        biasx = [antman.biasX for antman in Antz]
#        biasy = [antman.biasY for antman in Antz]
#        plt.hist2d(biasx, biasy, bins=11,cmap='hot',)
#        plt.colorbar()
#        plt.show()

        print(t,str(len(Antz)))

    [antman.updateLocation() for antman in Antz]
    EnvironmentUpdate()
