import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

from sklearn import decomposition
from sklearn import datasets
from sklearn.decomposition import PCA

import scipy
import scipy.io.wavfile

import os
from python_speech_features import mfcc

allpoints = np.zeros((0, 13), dtype = np.int16)

path1 = 'dataset/train/good/'
path2 = 'dataset/train/bad/'

print(allpoints.shape)

for filename in os.listdir(path1):
	rate, data = scipy.io.wavfile.read(path1 + filename)
	if data.ndim != 1:
		data = data[:, 0]
	features = mfcc(data, rate, nfft = 1200)
	print(features.shape)
	allpoints = np.append(allpoints, features, axis=0)

numgood = allpoints.shape[0]

for filename in os.listdir(path2):
        rate, data = scipy.io.wavfile.read(path2 + filename)
        if data.ndim != 1:
                data = data[:, 0]
        features = mfcc(data, rate, nfft = 1200)
        print(features.shape)
        allpoints = np.append(allpoints, features, axis=0)

numbad = allpoints.shape[0] - numgood

filename = "query.wav"
rate, data = scipy.io.wavfile.read(filename)
if data.ndim != 1:
	data = data[:, 0]
features = mfcc(data, rate, nfft = 1200)
print(features.shape)
allpoints = np.append(allpoints, features, axis=0)

numquery = allpoints.shape[0] - numbad - numgood

pca = PCA(3)  # project from 13 to 3 dimensions
projected = pca.fit_transform(allpoints)
print(allpoints.shape)
print(projected.shape)

rows = projected.shape[0]

fraction = 10
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["#f45041","#42adf4","#55f441"])
clist = [1]*numgood + [2]*numbad + [3]*numquery
subset = projected[range(0, rows, fraction), :]
clist = clist[0:rows:fraction]
sizes = [5]*(numgood+numbad) + [10]*numquery
sizes = sizes[0:rows:fraction]


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
ax.set_facecolor((.106,.1294,.17255))
ax.scatter(subset[:, 0], subset[:, 1], subset[:, 2], c=clist, cmap=cmap, s=sizes)
plt.show()
