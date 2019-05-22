import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

import pdb

from python_speech_features import mfcc, logfbank
from scipy.spatial import distance
from scipy.spatial import KDTree

(andre_rate, andre_sig) = wav.read("Matlab_Attempt/andre.wav")
andre_feat = mfcc(andre_sig, andre_rate)
andre_average_coeff = np.average(andre_feat, axis=0)

(andre_rate2, andre_sig2) = wav.read("Matlab_Attempt/andre2.wav")
andre_feat2 = mfcc(andre_sig2, andre_rate2)
andre_average_coeff2 = np.average(andre_feat2, axis=0)

(andre_rate3, andre_sig3) = wav.read("Matlab_Attempt/andre3.wav")
andre_feat3 = mfcc(andre_sig3, andre_rate3)
andre_average_coeff3 = np.average(andre_feat3, axis=0)

(kaelan_rate, kaelan_sig) = wav.read("Matlab_Attempt/kaelan.wav")
kaelan_feat = mfcc(kaelan_sig, kaelan_rate)
kaelan_average_coeff = np.average(kaelan_feat, axis=0)

(kaelan_rate2, kaelan_sig2) = wav.read("Matlab_Attempt/kaelan2.wav")
kaelan_feat2 = mfcc(kaelan_sig2, kaelan_rate2)
kaelan_average_coeff2 = np.average(kaelan_feat2, axis=0)

(bot_rate, bot_sig) = wav.read("Matlab_Attempt/hal.wav")
bot_feat = mfcc(bot_sig, bot_rate)
bot_average_coeff = np.average(bot_feat, axis=0)

#fbank_feat = logfbank(andre_sig, andre_rate)

plt.subplot(2,3,1)
plt.plot(andre_feat)
plt.subplot(2,3,2)
plt.plot(andre_feat2)
plt.subplot(2,3,3)
plt.plot(andre_feat3)
plt.subplot(2,3,4)
plt.plot(kaelan_feat)
plt.subplot(2,3,5)
plt.plot(kaelan_feat2)
plt.subplot(2,3,6)
plt.plot(bot_feat)

#f1 = plt.figure()
#f1.canvas.set_window_title('Andre')
#plt.plot(andre_feat)
#
#f2 = plt.figure()
#f2.canvas.set_window_title('Andre2')
#plt.plot(andre_feat2)
#
#f5 = plt.figure()
#f5.canvas.set_window_title('Andre3')
#plt.plot(andre_feat3)
#
#f3 = plt.figure()
#f3.canvas.set_window_title('Kaelan')
#plt.plot(kaelan_feat)
#
#f4 = plt.figure()
#f4.canvas.set_window_title('Bot')
#plt.plot(bot_feat)

print(distance.euclidean(andre_average_coeff, andre_average_coeff))
print(distance.euclidean(andre_average_coeff, andre_average_coeff2))
print(distance.euclidean(andre_average_coeff, andre_average_coeff3))
print(distance.euclidean(andre_average_coeff, kaelan_average_coeff))
print(distance.euclidean(andre_average_coeff, bot_average_coeff))

data = [andre_feat2, andre_feat3, kaelan_feat, kaelan_feat2, bot_feat]
lengths = list(map(len, data))
train = np.concatenate(data)
tree = KDTree(train)

closest_count = [0] * len(data)
for d in andre_feat:
    (dist, ind) = tree.query(d)
    for i, l in enumerate(lengths):
        ind -= l
        if ind < 0:
            closest_count[i] += 1
            break
print(closest_count)

#pdb.set_trace()

#plt.show()
