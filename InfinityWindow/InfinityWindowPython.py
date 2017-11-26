'''
Infinity Window
'''

import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams
rcParams['figure.figsize'] = 12,12
import itertools
from time import sleep

H = 10
W = 10
Window = [[0 for h in range(H)] for j in range(W)]

for h in range(H):
    for w in range(W):
        Window[h][w] = np.random.randint(2)

plt.matshow(Window, cmap = 'gray')

'''
Now how do we iterate through all the iterations of this window
'''

#%%
#flip = False
#c = 0
#for frame in itertools.product([0,1],repeat=H*W):
#    if c%10 == 0:
#        pic = np.array(frame)
#        flip = True
#        plt.imshow(pic.reshape(H,W), cmap = 'gray',interpolation='None')
#        plt.show()
#        print(c)
#    c+=1

#%%
c = 1000000000000000000050000000000
c = 633825300342584722313091090562 # Start from M
while True:
    c += 10
    pic = np.array(list(bin(c)))[2:].astype('int')
    plt.imshow(pic.reshape(H,W), cmap = 'gray',interpolation='None')
    plt.show()
    print(c)
#%%
'''
Phil implications
Library of babel
have all the informatjion
but is useless without a catalog
and it is quicker to discover it thann write a catalog
but as many right answers it contain, it contains as many wrong answers
---
Upper limit, how much information is contained here ?
H*W bits,
'''
