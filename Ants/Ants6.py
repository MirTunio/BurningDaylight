#INCOMPETANT ANTS!

from pylab import rcParams
import numpy as np
rcParams['figure.figsize'] = 9,3
from matplotlib import pyplot as plt


BoxX = 300
BoxY = 150
environment = np.array([[0. for i in range(BoxX)] for j in range(BoxY)])

'''
Environment Codes:
Food: -20
Pheramone trails: +ve number
Home: -10
NoGo: -30
'''
#%% ENVIRONMENT
#environment[20:45,150:175] = -20
environment[-25:, -25:] = -20
environment[:25,:25] = -10
plt.matshow(environment,cmap='hot',interpolation=None)
plt.show()

decayFactor = 0.60

def EnvironmentUpdate():
    pheramonesHere =  environment > 0
    environment[pheramonesHere] = environment[pheramonesHere] - decayFactor
    environment[-25:, -25:] = -20
    environment[:25,:25] = -10
    #environment[20:45,150:175] = -20

#Release ants at a constant rate
#%% ANT CLASS
class ant():
    global environment

    def __init__(self):
        self.biasX = 0
        self.biasY = 0
        self.pheramoneFUEL = 1500
        self.age = 12000000000000
        self.locY = np.random.randint(1,high=12)
        self.locX = np.random.randint(1,high=12)
        self.state = 'EXPLORE'
        self.speed = np.random.randint(10,40)

    def location(self):
        return self.locX,self.locY

    def updateLocation(self):
        self.age -= 1
        if self.age < 0:
            self.speed = np.random.randint(5,20)

        if self.state == 'EXPLORE':
            self.explore()
        elif self.state == 'FOODRUN':
            self.foodRun()
        else:
            raise ValueError('State invalid: %c' % self.state)

    def checklocX(self,xpos):
        if xpos <= 0:
            return 1

        if xpos >= BoxX-1:
            return BoxX-2

        return xpos

    def checklocY(self,ypos):
        if ypos <= 0:
            return 1

        if ypos >= BoxY-1:
            return BoxY-2
        return ypos

    def stepHere(self,xx,yy):
        if self.state == 'EXPLORE' and (xx > 275 and xx < 300) and (yy > 125 and yy < 150): # environment[yy,xx] == -20:
            self.pheramoneFUEL = 1500
            self.state = 'FOODRUN'
#
#        if self.state == 'EXPLORE' and (yy < 45 and yy > 20) and (xx > 150 and xx < 175): # environment[yy,xx] == -20:
#            self.pheramoneFUEL = 1500
#            self.state = 'FOODRUN'

        if self.state == 'FOODRUN' and (xx < 25 and xx > 0) and (yy < 25 and yy > 0): # environment[yy,xx] == -10
            self.pheramoneFUEL = 1500
            self.state = 'EXPLORE'

    def explore(self):
        self.spreadPheramone(self.locX,self.locY,20.)

        self.locX += np.random.randint(-1*self.speed*0.50,self.speed)
        self.locX += self.biasX
        self.locX = self.checklocX(self.locX)

        self.locY += np.random.randint(-1*self.speed*0.50,self.speed)
        self.locY += self.biasY
        self.locY = self.checklocY(self.locY)

        self.stepHere(self.locX,self.locY)
        self.setBias(self.locX,self.locY)

    def foodRun(self):
        self.spreadPheramone(self.locX,self.locY,20.)

        self.locX += np.random.randint(-1*self.speed,self.speed*0.50)
        self.locX += self.biasX
        self.locX = self.checklocX(self.locX)

        self.locY += np.random.randint(-1*self.speed,self.speed*0.50)
        self.locY += self.biasY
        self.locY = self.checklocY(self.locY)

        self.stepHere(self.locX,self.locY)
        self.setBias(self.locX,self.locY)

    def spreadPheramone(self,centerX,centerY,amount):
        kernelX = [centerX-1,centerX,centerX+1]
        kernelY = [centerY-1,centerY,centerY+1]

        if (self.pheramoneFUEL - amount) > 0:
            environment[kernelY,kernelX] += amount
            self.pheramoneFUEL -= amount


    def setBias(self,xx,yy):
        xscanpos = environment[yy,xx:xx+200]
        xscanneg = environment[yy,xx-200:xx]
        yscanpos = environment[yy:yy+200,xx]
        yscanneg = environment[yy-200:yy,xx]

        xscanpos = np.sum(xscanpos[xscanpos>0])
        xscanneg = np.sum(xscanneg[xscanneg>0])
        yscanpos = np.sum(yscanpos[yscanpos>0])
        yscanneg = np.sum(yscanneg[yscanneg>0])

        if xscanpos > xscanneg+2:
            self.biasX = np.random.randint(10)
        elif xscanneg > xscanpos+2:
            self.biasX = -1*np.random.randint(10)
        else:
            self.biasX = 0

        if yscanpos > yscanneg+2:
            self.biasY = np.random.randint(10)
        elif yscanneg > yscanpos+2:
            self.biasY = -1*np.random.randint(10)
        else:
            self.biasY = 0

# NEXT CHANGE WILL BE TO FINE TUNE THE BIAS

#%% RUN
Time = 10000000
Antz = [ant() for i in range(3)]
splorelog = []

#%%
for t in range(Time):
    if t%100 == 0:
        Antz.append(ant())
        Antz.append(ant())
#        print('New Ants!')

    if t%(5) == 0 and t > 10000:#500: #0:# 10
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

        plt.matshow(environmentoverlay,cmap='plasma',vmin=-150,vmax=10000)#400)#3000)
        plt.colorbar()
        plt.title('Exploring Now: ' + str(explorenum) + ' of ' + str(allnum))# + ' ' + str(pheramonenum))
        plt.show()

        plt.hist2d(anty, antx, bins=50,cmap='hot',range = [[0, 150], [0, 300]],vmin=0,vmax=5)
        plt.colorbar()
        plt.show()
#
#        biasx = [antman.biasX for antman in Antz]
#        biasy = [antman.biasY for antman in Antz]
#        plt.hist2d(biasx, biasy, bins=11,cmap='hot',)
#        plt.colorbar()
#        plt.show()

        print(t,str(len(Antz)))

    [antman.updateLocation() for antman in Antz]
    EnvironmentUpdate()
