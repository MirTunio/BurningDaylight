# State Space Reconstruction
'''
Method:
	Input: 
		Time series
	Algorithm:
		Time-Delay Embedding:
			lenght = len(time series)
			dimensions = range(1,lenght)
			for dimensions D:
				dimset = [lenght/D x D]
				
				for modval = range(0,D):
					for row in range(0,length/D):
						modsample = [time series[i] for i in range(lenght) if i%modval == 0]
						dimset[:][modval] = modsample
'''

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 11,8.5
from mpl_toolkits.mplot3d import Axes3D
import glob
import time

files = glob.glob('b*')

b1 = pd.read_table(files[0],delimiter = ' ', names = ["Rate","Volume","o2","delme"])
#b2 = pd.read_table(files[1],delimiter = ' ', names = ["Rate","Volume","o2","delme"])
del b1['delme']
#del b2['delme']

data = b1.copy().Rate

L = len(data)
Embeddings = []

for d in np.arange(300,301,1):
	print(d)
	Embedding = []

	for modval in np.arange(d):
		modsample = [data[i] for i in np.arange(L) if (i+modval)%d == 0]
		Embedding.append(modsample)

	Embedding_df = pd.DataFrame(Embedding).transpose()
	Embeddings.append(Embedding_df)
				
#%% DEMONSTRATE MOTHAFUCKA

#for i in np.arange(1,10):#np.arange(0,len(Embeddings)):
#    print(i)
#    dimbed = Embeddings[i]
#    axes = dimbed.columns
#    for j in axes:
#        k = dimbed[j]
#        plt.plot(k.values,color=(float(j)/len(axes),1-float(j)/len(axes),0.1),alpha=0.5)
#    plt.show()
#	#plt.savefig(str(i))
#	#plt.cla()
#	#plt.clf()
#    print(str(i))
#%%

for k in Embeddings:
    cols = k.columns
    
    if len(cols)<2:
        k.plot()
        continue
    


    for i in np.arange(0,len(cols)-2,10):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(k[cols[i]],k[cols[i+1]],k[cols[i+2]], c='r', marker='o')
        #ax.title('dimbed: ' + str(len(cols)) + ' colpair:' + str(i) + ',' + str(i+1), ',', str(i+2))
        plt.show()
        time.sleep(0.1)
        print('dimbed: ' + str(len(cols)), ' colpair:' + str(i), str(i+1), str(i+2))
        
    
    






