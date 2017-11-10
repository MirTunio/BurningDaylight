#Keyboard Audio Work
import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


p = pyaudio.PyAudio()
pyaudio.paDirectSound = 1

#Opens stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

#Saves stream at appropriate rate to a list
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

#Closes the stream
stream.stop_stream()
stream.close()
p.terminate()

#Saves to wav file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()