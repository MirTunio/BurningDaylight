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


data = pd.read_csv('data.csv')['TimeSeries'].values

L = len(data)
Embeddings = []

for d in np.arange(365):
	print(d)
	Embedding = []

	for modval in np.arange(d):
		modsample = [data[i] for i in np.arange(L) if (i+modval)%d == 0]
		Embedding.append(modsample)

	Embedding_df = pd.DataFrame(Embedding).transpose()
	Embeddings.append(Embedding_df)
				
#%% DEMONSTRATE MOTHAFUCKA

for i in [5,10,20,62,125,250,363]:#np.arange(0,len(Embeddings)):
	dimbed = Embeddings[i]
	axes = dimbed.columns
	for j in axes:
		k = dimbed[j]
		plt.plot(np.log(k.values),color=(float(j)/len(axes),1-float(j)/len(axes),0.1),alpha=0.5)
		
	plt.savefig(str(i))
	plt.cla()
	plt.clf()

	print(str(i))				

#%%
