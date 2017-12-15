'''
Ant trails
'''
from pylab import rcParams
import numpy as np
rcParams['figure.figsize'] = 10,10
from matplotlib import pyplot as plt

#%% Setup
#Terrain = 0
#Pheramone intensity is number value
#Food source is -10
#Colony is -20

width = 50
height = 50
terrain = np.array([[0 for i in range(width)] for j in range(height)])
ants = []

terrain[np.random.randint(width)][np.random.randint(height)] = -10
terrain[height-1][0] = -20


class Ant():
    locx = 0
    locy = 0
    direction = 0
    speed = 1

    def __init__(self, locx, locy,direction):
        self.locx = locx
        self.locy = locy
        self.direction = direction

    def update(self):
        newx = self.locx + self.speed*np.sin(self.direction)+np.random.random()-0.5
        newy = self.locy + self.speed*np.cos(self.direction)+np.random.random()-0.5

        if newx > width:
            self.direction = self.direction - np.pi+self.direction
            newx = self.locx + self.speed*np.sin(self.direction)+np.random.random()-0.5
        if newy > height:
            self.direction = self.direction - np.pi+self.direction
            newy = self.locy + self.speed*np.cos(self.direction)+np.random.random()-0.5
        if newx < 0:
            self.direction = self.direction + np.pi+self.direction
            newx = self.locx + self.speed*np.sin(self.direction)+np.random.random()-0.5+self.direction
        if newy < 0:
            self.direction = self.direction + np.pi+self.direction
            newy = self.locy + self.speed*np.cos(self.direction)+np.random.random()-0.5+self.direction

        self.locx = newx
        self.locy = newy



for i in range(1):
    ants.append(Ant(height-1,0,(1.5)*np.pi+(np.pi/2)*np.random.random()))

for ant in ants:
    terrain[ant.locx][ant.locy] = 1



plt.matshow(terrain)

for i in range(1000):
    for ant in ants:
        ant.update()
    for ant in ants:
        try:
            terrain[ant.locx][ant.locy] = 1
        except:
            pass

    plt.matshow(terrain)
    plt.show()
    print(i)

