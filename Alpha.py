#REALL make thus abstracted an dexpandedavble

#Back into the groove
#fake signal: random + perlin noise
#random algo
#work on markers

import time
import random
import numpy as np


def signal():
    return 100*random.random()
    
    
def alg():
    if movingaverage() == 1:
        sell()
    if movingaverage() == 2:
        buy()
    if movingaverage() == 3:
        hold()
    
def buy():
    print('buy')
def sell():
    print('sell')
def hold():
    print('hold')
    
def movingaverage():
    return 3
    
class account():
    # contains name
    # contains money
    # contains holdings
    # initialize with strategy
    