import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

from python_speech_features import mfcc, logfbank
from scipy.spatial import distance

(rate,sig) = wav.read("test.wav")

mfcc_feat = mfcc(sig, rate)
average_coeff = np.average(mfcc_feat, axis=0)

fbank_feat = logfbank(sig, rate)

plt.plot(fbank_feat)
plt.show()
