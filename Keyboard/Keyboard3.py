#Need to make a threshold trigger to register an event and also record the key press
#Using the livespec sampling length will not owkr
#Look up eg on how to record when triggered, set low threshold and see what happens
#make a large data set I guess

#I can solve this now.

# Step 1:
# Get microphone working
# 
# Step 2:
# Make a neat way to collect data all the fucking time
#
# Step 3:
# Orgnaize the collected data 
# 
# Step 4:
# Train the mother fucker!
#%%

import pyaudio
import numpy as np
from matplotlib import pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 10,10

x = 0 
while x < 400:
	a = pyaudio.PyAudio()
	stream = a.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=2048)
	data = stream.read(2048)
	y = np.fromstring(data, 'int16')
	
	if max(y) > 3000:
		plt.plot(y)
		plt.show()
		print(y)
		x+=1
		