#Bees
'''
True stability is borne out of the interplay of opposing forces. Too much homogeneity breeds instability.
'''
import numpy as np
from matplotlib import pyplot as plt

HiveT = 39 #Starting temperature

class Bees:
    def __init__(self,dist):
        self.dist = dist
        if self.dist:
            self.gtI = np.random.normal(loc = 30.12311, scale = 6) #Randomly distributed ideal temperatures about the true hive ideal
        else:
            self.gtI = 30.12311 #All ideal temperatures exactly the hive ideal temperature

    def HorC(self,HT): #Each bees internal thermostat, HT is the Hive Temperature
        self.heat = False
        self.cool = False
        self.stay = True

        if HT > self.gtI:
            self.cool = True

        if HT < self.gtI:
            self.heat = True

        if HT == self.gtI:
            self.stay = True
            self.cool = False
            self.heat = False


#SET ranno to False for NO genetic variety
#SET ranno to True for genetic variety
#OBSERVE the lack of stability when there is lack of genetic variety

def trial(iterations,ranno,HiveT): #Look at the amount of bees cooling and heating, and then change the hive temperature accordingly
    BeeNum = 100. #The number of bees
    Tray = np.array([]) #Holds the historical temperature of the hive
    Hive = [Bees(ranno) for i in np.arange(BeeNum)] #Fills the hive with bees

    for i in np.arange(iterations): #See what each bee's thermostat feels about the temperature
        for bee in Hive:
            bee.HorC(HiveT)

        Heaters = [bee.heat for bee in Hive] #List of bees heating the hive
        Coolers = [bee.cool for bee in Hive] #List of bees cooling the hive   

        heatp = np.count_nonzero(Heaters) #The number of bees heating the hive
        coolp = np.count_nonzero(Coolers) #The number of bees cooling the hive

        HiveT = HiveT + heatp/BeeNum - coolp/BeeNum #Adjust the hive temperature accordingly
        Tray = np.append(Tray,HiveT) #Add temperature to log
        
    plt.plot(Tray) # The following lines plots the temperature log
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.show()








