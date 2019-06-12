import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

import pdb

from python_speech_features import mfcc, logfbank
from scipy.spatial import distance
from scipy.spatial import KDTree

(andre_rate, andre_sig) = wav.read("dataset/train/good/andre.wav")
andre_feat = mfcc(andre_sig, andre_rate)
andre_average_coeff = np.average(andre_feat, axis=0)

(andre2_rate, andre2_sig) = wav.read("dataset/train/good/andre2.wav")
andre2_feat = mfcc(andre2_sig, andre2_rate)
andre2_average_coeff = np.average(andre2_feat, axis=0)

(andre3_rate, andre_sig3) = wav.read("dataset/train/good/andre3.wav")
andre3_feat = mfcc(andre_sig3, andre3_rate)
andre3_average_coeff = np.average(andre3_feat, axis=0)

(kaelan_rate, kaelan_sig) = wav.read("dataset/train/good/kaelan.wav")
kaelan_feat = mfcc(kaelan_sig, kaelan_rate)
kaelan_average_coeff = np.average(kaelan_feat, axis=0)

(kaelan2_rate, kaelan2_sig) = wav.read("dataset/train/good/kaelan2.wav")
kaelan2_feat = mfcc(kaelan2_sig, kaelan2_rate)
kaelan2_average_coeff = np.average(kaelan2_feat, axis=0)

(bot_rate, bot_sig) = wav.read("dataset/train/bad/bothello.wav")
bot_feat = mfcc(bot_sig, bot_rate)
bot_average_coeff = np.average(bot_feat, axis=0)

(bot2_rate, bot2_sig) = wav.read("dataset/train/bad/narrator.wav")
bot2_feat = mfcc(bot2_sig, bot2_rate)
bot2_average_coeff = np.average(bot2_feat, axis=0)

(bot3_rate, bot3_sig) = wav.read("dataset/train/bad/siri.wav")
bot3_feat = mfcc(bot3_sig, bot3_rate)
bot3_average_coeff = np.average(bot3_feat, axis=0)

(human_rate, human_sig) = wav.read("dataset/train/good/femalevoice.wav")
human_feat = mfcc(human_sig, human_rate)
human_average_coeff = np.average(human_feat, axis=0)

(test_rate, test_sig) = wav.read("dataset/human/homer1.wav")
test_feat = mfcc(test_sig, test_rate)
test_average_coeff = np.average(test_feat, axis=0)

#fbank_feat = logfbank(andre_sig, andre_rate)

#f1 = plt.figure()
#f1.canvas.set_window_title('Andre')
#plt.plot(andre_feat)
#
#f2 = plt.figure()
#f2.canvas.set_window_title('Andre2')
#plt.plot(andre2_feat)
#
#f5 = plt.figure()
#f5.canvas.set_window_title('Andre3')
#plt.plot(andre3_feat)
#
#f3 = plt.figure()
#f3.canvas.set_window_title('Kaelan')
#plt.plot(kaelan_feat)
#
#f4 = plt.figure()
#f4.canvas.set_window_title('Bot')
#plt.plot(bot_feat)

#print(distance.euclidean(andre_average_coeff, andre_average_coeff))

data = [andre_feat, andre2_feat, andre3_feat, kaelan_feat, kaelan2_feat, bot2_feat, bot3_feat]
lengths = list(map(len, data))
train = np.concatenate(data)
tree = KDTree(train)

closest_count = [0] * len(data)
for d in test_feat:
    (dist, ind) = tree.query(d)
    for i, l in enumerate(lengths):
        ind -= l
        if ind < 0:
            closest_count[i] += 1
            break
print(closest_count)

#pdb.set_trace()

plt.subplot(2,3,1)
plt.plot(andre_feat)
plt.subplot(2,3,2)
plt.plot(andre2_feat)
plt.subplot(2,3,3)
plt.plot(andre3_feat)
plt.subplot(2,3,4)
plt.plot(bot_feat)
plt.subplot(2,3,5)
plt.plot(bot2_feat)
plt.subplot(2,3,6)
plt.plot(test_feat)

plt.show()
