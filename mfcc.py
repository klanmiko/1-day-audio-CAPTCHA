from python_speech_features import mfcc
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

(rate,sig) = wav.read("test.wav")
mfcc_feat = mfcc(sig,rate)

print(mfcc_feat)
plt.plot(mfcc_feat)
plt.show()
