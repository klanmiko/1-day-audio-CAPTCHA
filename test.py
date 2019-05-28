import pyogg
import audioop
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

opus = pyogg.OpusFile('./speech.ogg')
buffer = np.ctypeslib.as_array(opus.buffer, shape=(opus.buffer_length,))
# f, t, Sxx = signal.spectrogram(x, fs=fs)
print(buffer / 1000)
f, t, Sxx = signal.spectrogram(buffer / 1000, fs=opus.frequency, window=('hamming'))
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()