"""
Dec 20 2022
A module to listen to the mic.
"""

import pyaudio
import os

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS=1
RATE=16000

p=pyaudio.PyAudio()

stream=p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=0,
    frames_per_buffer=FRAMES_PER_BUFFER
    )

def hark(_duration):
    seconds=_duration
    frames=[]
    for i in range(0,int(RATE/FRAMES_PER_BUFFER*seconds)):
        data=stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
    return frames
    stream.stop_stream()
    stream.close()
    p.terminate()

print(hark(5))