'''
Ant trails

What are we trying to do?
Want to simulate ants finding food, by leaving a constantly evaporating
trail of pheramones.
Want to observe the trail converge to the fastest path!
Need to develop a model for this ant creature
What behaviours do I have to model?

Ant:
Leaves a weak trail along all wonderings
Leaves strong trail of pheramones once food is found
Proclivity to follow pheramone trails
NEEDS a sense of where it can/should step (will allow bridges) [STEPCHECKA]
NEEDS to follow a random search pattern from the ant hill
What do we do when food found? -> Only allow steps down & left
^IMPLIES only steps up & right when no food
^IMPLIES colony in BottomLeft, food in Top Left
::Step allowing should be noisy, not random.

Environment:
Holds pheramones and decays presence at constant rate
Holds locations of food
Need to handle boundries wisely (Just dissalow steps..okay)
'''

from pylab import rcParams
import numpy as np
rcParams['figure.figsize'] = 9,3
from matplotlib import pyplot as plt

#%% SETUP
BoxX = 800
BoxY = 400
environment = np.array([[0 for i in range(BoxX)] for j in range(BoxY)])

'''
Environment Codes:
Food: -20
Pheramone trails: +ve number
Home: -10
NoGo: -30
'''
environment[350:,750:] = -20
environment[:50,:50] = -10
environment[0,:] = -30
environment[:,0] = -30
environment[399,:] = -30
environment[:,799] = -30
environment = np.array(environment)

plt.matshow(environment,cmap='hot',interpolation=None)
plt.show()

'''
Ant needs to have states [WANDER, FOODFOUND]
Environment updating first:
'''
#%% ENVIRONMENT HANDLING
decayFactor = 0.95

def EnvironmentUpdate():
    pheramonesHere =  environment > 0
    environment[pheramonesHere] = environment[pheramonesHere]*decayFactor

    pheramonesTooMany = environment > 100
    environment[pheramonesTooMany] = 100
    environment[350:,750:] = -20
    environment[:50,:50] = -10
    environment[0,:] = -30
    environment[:,0] = -30
    environment[399,:] = -30
    environment[:,799] = -30

#%%ENVIRONMENT PHERAMONE DECAY TESTING
#environment[50:70,50:70] = 2
#environment[100:120,50:70] = 1
#for i in range(10):
#    plt.matshow(environment,cmap='afmhot',interpolation=None)
#    plt.show()
#    EnvironmentUpdate()
#    print(i)

#%% ANTZ

class ant():
    global environment
    biasX = 0
    biasY = 0

    def __init__(self):
        self.locY = np.random.randint(1,high=100)
        self.locX = np.random.randint(1,high=100)
        self.state = 'EXPLORE'
        self.speed = np.random.randint(50)

    def location(self):
        return self.locX,self.locY

    def updateLocation(self):
        if self.state == 'EXPLORE':
            self.explore()
        elif self.state == 'GOHOME':
            self.goHome()
        else:
            raise ValueError('State invalid: %c' % self.state)

    def explore(self):
        self.spreadPheramone(self.locX,self.locY,30)
        self.setBias(self.locX,self.locY)

        self.locX += np.random.randint(2,50+self.speed)
#        self.locX += self.biasX
        self.locX = self.checklocX(self.locX)

        self.locY += np.random.randint(2,50+self.speed)
#        self.locY += self.biasY
        self.locY = self.checklocY(self.locY)

        self.stepHere(self.locX,self.locY)

    def goHome(self):
        self.spreadPheramone(self.locX,self.locY,70)
        self.setBias(self.locX,self.locY)

        self.locX -= np.random.randint(2,40+self.speed)
        self.locX += self.biasX
        self.locX = self.checklocX(self.locX)

        self.locY -= np.random.randint(2,40+self.speed)
        self.locY += self.biasY
        self.locY = self.checklocY(self.locY)

        self.stepHere(self.locX,self.locY)

    def checklocX(self,xpos):
        if xpos <= 0:
            return 1

        if xpos >= 799:
            return 798

        return xpos

    def checklocY(self,ypos):
        if ypos <= 0:
            return 1

        if ypos >= 399:
            return 398

        return ypos

    def stepHere(self,xx,yy):
        if self.state == 'EXPLORE' and (yy>=350) and (xx>=750):# and environment[yy,xx] == -20:
            self.state = 'GOHOME'

        if self.state == 'GOHOME' and (yy<=50) and (xx<=50):#and environment[yy,xx] == -10:
            self.state = 'EXPLORE'

    def spreadPheramone(self,centerX,centerY,amount):
        kernelX = [self.locX-1, self.locX-1, self.locX-1,
                   self.locX, self.locX, self.locX,
                   self.locX+1, self.locX+1, self.locX+1]

        kernelY = [self.locY-1,self.locY,self.locY+1,
                   self.locY-1,self.locY,self.locY+1,
                   self.locY-1,self.locY,self.locY+1,]
        environment[kernelY,kernelX] += amount #20

    def setBias(self,xx,yy):
        scanxneg = np.dot([self.filt(x) for x in environment[yy,xx-250:xx]],[1 for x in np.arange(1,len(environment[yy,xx-250:xx])+1)])
        scanxpos = np.dot([self.filt(x) for x in environment[yy,xx:xx+250]],[1 for x in np.arange(1,len(environment[yy,xx:xx+250])+1)])
        scanyneg = np.dot([self.filt(x) for x in environment[yy-250:yy,xx]],[1 for x in np.arange(1,len(environment[yy-250:yy,xx])+1)])
        scanypos = np.dot([self.filt(x) for x in environment[yy:yy+250,xx]],[1 for x in np.arange(1,len(environment[yy:yy+250,xx])+1)])

        self.biasX = 60*( float((scanxpos-scanxneg)/(scanxpos+scanxneg))/(1+np.sum(np.abs(environment[yy,xx-250:xx+250]))))-20
        self.biasY = 60*( float((scanypos-scanyneg)/(scanypos+scanyneg))/(1+np.sum(np.abs(environment[yy-250:yy+250,xx]))))-20

    def filt(self,num):
        if num > 0:
            return num
        else:
            return 0

#%% ANT LOCATION TESTING
#juice = [ant() for i in range(1000)]
#for antz in juice:
#    plt.scatter(*antz.location())
#plt.show()


#%% RUN
Time = 30000
Antz = np.array([ant() for i in range(100)])
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

        plt.matshow(environmentoverlay,cmap='hot',vmin=0,vmax=50)
        plt.title('Exploring Now: ' + str(explorenum))
        plt.show()

        plt.hist2d(anty, antx, bins=50,cmap='hot')
        plt.colorbar()
        plt.show()

        biasx = [antman.biasX for antman in Antz]
        biasy = [antman.biasY for antman in Antz]
        plt.hist2d(biasx, biasy, bins=11,cmap='hot',range = [[-40, 40], [-40, 40]])
        plt.colorbar()
        plt.show()

        print(t)

    [antman.updateLocation() for antman in Antz]
    EnvironmentUpdate()



#%%

plt.plot(splorelog)
plt.show()

plt.hist(antx,bins=100)
plt.title('XPOS')
plt.show()

plt.hist(anty,bins=100)
plt.title('YPOS')
plt.show()











