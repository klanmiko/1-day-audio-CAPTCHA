import pyogg
import audioop
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
import wave
import ctypes

opus = pyogg.OpusFile('./speech.ogg')
print(opus.buffer_length)
bfarr_t = ctypes.c_int16*(int(opus.buffer_length / 2))
bf = bfarr_t.from_buffer(ctypes.pointer(opus.buffer))

with wave.open('./speech.wav', 'wb') as writer:
  writer.setnchannels(opus.channels)
  writer.setframerate(opus.frequency)
  writer.setsampwidth(2)
  writer.writeframesraw(a)

with wave.open('./speech.wav', 'rb') as reader:
  print(reader.getparams())