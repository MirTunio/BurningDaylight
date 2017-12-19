# INCOMPETANT ANTS!
'''
Simulation of ant pathfinding phenomenon. The ants leave the hive at regular
intervals, depositing a pheromone trail as they go, to find sources of food.
Once a source of food has been found the return to the hive. Each ant is
biased to follow a pheromone trail which is constantly evaporating.
I tried to create the following simulation with as few moving parts as
possible, and kept the rule-sets for each ant binary as far as it was
reasonable. This is the second version that worked reasonably well, however
there are several aspects which need to be worked on. More details at:
https://medium.com/burningdaylight/ants-1-43812fd1ea0f

'''

from pylab import rcParams
import numpy as np
rcParams['figure.figsize'] = 5,5
from matplotlib import pyplot as plt
from noise import pnoise1

#%% TERRAIN SETUP

BoxX = 200 #Width of terrain
BoxY = 200 #Height of terrain
environment = np.array([[0. for i in range(BoxX)] for j in range(BoxY)]) #Creating array for terrain

'''
Environment Codes:
Food: -20
Pheramone trails: +ve number
Home: -10
NoGo: -30
'''
#Setting up the environment so that the ant-hill and food sources have a strong
#pheromonal signature
environment[5:15,95:106] = 1000
environment[80:90,120:130] = 1000
environment[81:91,71:81] = 1000
plt.matshow(environment,cmap='hot',interpolation=None)
plt.show()

decayFactor = 0.025 #Rate at which pheromone evaporates

#Function to update the environment each iteration, can be changed to allow the food source to deplete
def EnvironmentUpdate():
    pheramonesHere =  environment > 0
    environment[pheramonesHere] = environment[pheramonesHere] - decayFactor
    environment[5:15,95:106] = 1000
    environment[80:90,120:130] = 1000
    environment[81:91,71:81] = 1000

#Creating an overlay for the ant-class to tell whether it is on food pixel or a ant-hill pixel
environmentmap = np.array([[0. for i in range(BoxX)] for j in range(BoxY)])
environmentmap[5:5,95:106] = -10
environmentmap[80:90,120:130] = -20
environmentmap[81:91,71:81] = -20

#%% ANT CLASS

class ant():
    global environment
    global environmentmap

    def __init__(self): #Intialize ant randomly inside the colony
        self.biasX = 0
        self.biasY = 0
        self.locY = np.random.randint(5,high=16)
        self.locX = np.random.randint(95,high=106)
        self.state = 'EXPLORE'

    def updateLocation(self): #Used to shunt ant towards correct behaviour based on state
        if self.state == 'EXPLORE':
            self.explore()
        elif self.state == 'FOODRUN':
            self.foodRun()
        elif self.state == 'DEAD':
            self.dead()

    def checklocX(self,xpos): #What to do at X boundaries
        if xpos <= 0:
            self.state = 'DEAD'
            return 1
        if xpos >= BoxX-1:
            self.state = 'DEAD'
            return BoxX-2
        return xpos

    def checklocY(self,ypos): #What to do at Y boundaries
        if ypos <= 0:
            self.state = 'DEAD'
            return 1
        if ypos >= BoxY-1:
            self.state = 'DEAD'
            return BoxY-2
        return ypos

    def stepHere(self,xx,yy): #Flip states when found food or returned home after finding food
        xx = int(np.floor(xx))
        yy = int(np.floor(yy))

        if self.state == 'EXPLORE' and environmentmap[yy,xx] == -20:
            self.state = 'FOODRUN'

        if self.state == 'FOODRUN' and environmentmap[yy,xx] == -10:
            self.state = 'EXPLORE'

    def dead(self): #Respawns the ant inside the colony
        self.locY = np.random.randint(5,high=15)
        self.locX = np.random.randint(95,high=106)
        self.state = 'EXPLORE'

    def explore(self): #Food finding state
        self.setBias(self.locX,self.locY) #Set the bias parameters
        self.spreadPheramone(self.locX,self.locY,.5) #deposits 0.5 pheromone when exploring
        self.locX += np.random.randint(-5,6) + self.biasX #move randomly in X and add bias according to local pheromone environment
        self.locX = self.checklocX(self.locX) #Check if a X boundary was hit
        self.locY += np.random.randint(-5,6) + self.biasY + np.random.randint(5) #Move randomly in Y and add bias
        self.locY = self.checklocY(self.locY)#Check if a Y boundary was hit
        self.stepHere(self.locX,self.locY) #Check if the ant is at a food source or in the colony

    def foodRun(self): #Returning food to colony state
        self.setBias(self.locX,self.locY)
        self.spreadPheramone(self.locX,self.locY,4.) #deposits 4.0 pheromone when food is found
        self.locX += np.random.randint(-5,6) + self.biasX
        self.locX = self.checklocX(self.locX)
        self.locY += np.random.randint(-5,6) + self.biasY - np.random.randint(5)
        self.locY = self.checklocY(self.locY)
        self.stepHere(self.locX,self.locY)

    def spreadPheramone(self,xx,yy,amount): #Deposit pheromones on the environment
        xx = int(np.floor(xx))
        yy = int(np.floor(yy))
        environment[yy,xx] += amount

    def setBias(self,xx,yy): #Scan local environment for pheromones and set bias
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
Antz = [ant() for i in range(10)] #Intialize with 10 ants
splorelog = []

#%%
for t in range(Time):
    if t%30 == 0: #Add 6 ants every 30 iterations
        Antz.append(ant())
        Antz.append(ant())
        Antz.append(ant())
        Antz.append(ant())
        Antz.append(ant())
        Antz.append(ant())

    if t%(10) == 0: #Plotting utility
        environmentoverlay = environment.copy()
        antx = [antman.locX for antman in Antz]
        anty = [antman.locY for antman in Antz]

        environmentoverlay[anty,antx] = 2

        explorenum = np.count_nonzero([antman.state == 'EXPLORE' for antman in Antz])
        allnum = len(Antz)
        splorelog.append(explorenum)

        plt.matshow(environmentoverlay,cmap='plasma',vmin=-5,vmax=10) #To view pheromones and environment
        plt.colorbar()
        plt.title('Exploring Now: ' + str(explorenum) + ' of ' + str(allnum))
        plt.show()

#        plt.hist2d(anty, antx, bins=50,cmap='hot',range = [[0, 200], [0, 200]],vmin=0,vmax=5) #To view locations of ants
#        plt.show()
#
#        biasx = [antman.biasX for antman in Antz] #To track the biases of all the ants live
#        biasy = [antman.biasY for antman in Antz]
#        plt.hist2d(biasx, biasy, bins=11,cmap='hot',)
#        plt.colorbar()
#        plt.show()

        print(t,str(len(Antz)))

    [antman.updateLocation() for antman in Antz] #Update location of each ant
    EnvironmentUpdate() #Update the environment
