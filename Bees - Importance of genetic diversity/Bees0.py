#Bees
import numpy as np
from matplotlib import pyplot as plt

HiveT = 30

class Bees:
    def __init__(self,dist):
        self.dist = dist
        if self.dist:
            self.gtH = np.random.normal(loc = 35., scale = 6) #genetic threshold
            self.gtL = np.random.normal(loc = 25., scale = 6)
        else:
            self.gtH = 35
            self.gtL = 25
    
    def HorC(self,HT):
        self.heat = False
        self.cool = False
        self.stay = True
        
        if HT > self.gtH:
            self.cool = True
        
        if HT < self.gtL:
            self.heat = True
        
        if HT < self.gtH and HT > self.gtL:
            self.stay = True
        


def trial(iterations,ranno,HiveT): #look at the amount of bees cooling and heating, and then cahnge the Hivetemeprature accrodingl
    BeeNum = 100.
    Tray = np.array([])
    Hive = [Bees(ranno) for i in np.arange(BeeNum)]
        
    for i in np.arange(iterations):           
        for bee in Hive:
            bee.HorC(HiveT)
        
        Heaters = [bee.heat for bee in Hive]
        Coolers = [bee.cool for bee in Hive]
    
        #print(Heaters, Coolers,HiveT)
    
        heatp = np.count_nonzero(Heaters)
        coolp = np.count_nonzero(Coolers)
    
        #print(heatp,coolp)
        HiveT = HiveT + heatp/BeeNum - coolp/BeeNum
        Tray = np.append(Tray,HiveT)
        #print(HiveT)
    plt.plot(Tray)
    
    
    
    
    
    
    
    
    