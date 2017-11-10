#Keyboard Audio Work
import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt
import struct


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


p = pyaudio.PyAudio()
pyaudio.paDirectSound = 1

#Opens stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

ray = []
for i in np.arange(1000):
    data = stream.read(1)
    y = np.fromstring(data, 'int16')
    ray = np.append(ray,y)
    #print(valu)
plt.plot(ray)



#Closes the stream
stream.stop_stream()
stream.close()
p.terminate()
