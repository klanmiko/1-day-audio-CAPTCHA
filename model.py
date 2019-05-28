import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

import pdb
import os

from python_speech_features import mfcc, logfbank
from scipy.spatial import distance
from scipy.spatial import KDTree

from sklearn.mixture import GaussianMixture

good_dir = os.path.join(os.path.curdir, "dataset", "train", "good")
bad_dir = os.path.join(os.path.curdir, "dataset","train", "bad")

def extract_features(audio):
  (rate, sig) = wav.read(audio)
  features = mfcc(sig, rate, nfft=1024)
  return features

def k_argmax(array, k):
  if k < len(array):
    raise IndexError()
  elif k == len(array):
    return np.argsort(array).tolist()

  argmax = [-1] * (k + 1)
  for i in range(len(array)):
    val = array[i]
    for j in range(k):
      if argmax[k - j] == -1 or val >= array[argmax[k - j]]:
        argmax[k - j + 1] = array[argmax[k - j]]
      elif val < array[argmax[k - j]]:
        argmax[k - j + 1] = i
    if val > array[argmax[0]]:
      argmax[0] = i
  return argmax[0:k]

class Model():
  def train(self):
    self.good_data = []
    self.bad_data = []
    for audio in os.listdir(good_dir):
        self.good_data.append(extract_features(os.path.join(good_dir, audio)))

    for audio in os.listdir(bad_dir):
        self.bad_data.append(extract_features(os.path.join(bad_dir, audio)))

    self.data = self.good_data + self.bad_data
    train = np.concatenate(self.data)
    self.tree = KDTree(train)

    self.GMM_good = GaussianMixture(n_components=3, covariance_type='full', n_init=3, max_iter=1000, tol=1e-4)
    self.GMM_good.fit(np.concatenate(self.good_data))

    self.GMM_bad = GaussianMixture(n_components=3, covariance_type='full', n_init=3, max_iter=1000, tol=1e-4)
    self.GMM_bad.fit(np.concatenate(self.bad_data))

  def label(self, audio):
    feat = extract_features(audio)
    closest_count = [0] * len(self.data)
    lengths = list(map(len, self.data))
    for d in feat:
        (dist, ind) = self.tree.query(d)
        for i, l in enumerate(lengths):
            ind -= l
            if ind < 0:
                closest_count[i] += 1
                break
    print(closest_count)
    try:
      kNN = k_argmax(closest_count, 3)
      print(kNN)
      good_count = 0
      bad_count = 0
      for k in range(len(kNN)):
        if kNN[k] < len(self.good_data):
          good_count += 1
        else:
          bad_count += 1
    except:
      pass
      
    gscore = self.GMM_good.score(feat)
    bscore = self.GMM_bad.score(feat)

    score = gscore - bscore

    return 'good' if score > 0 else 'bad'