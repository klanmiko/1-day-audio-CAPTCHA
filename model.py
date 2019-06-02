import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

import pdb
import os

from python_speech_features import mfcc, logfbank, delta
from scipy.spatial import distance
from sklearn.neighbors import KNeighborsClassifier

from sklearn.mixture import GaussianMixture

good_dir = os.path.join(os.path.curdir, "dataset", "train", "good")
bad_dir = os.path.join(os.path.curdir, "dataset","train", "bad")

def extract_features(audio):
  (rate, sig) = wav.read(audio)
  features = mfcc(sig, rate, nfft=1024)
  d = delta(features, 2)
  return list(map(lambda x, y: x + y, features, d))

class Model():
  def train(self):
    self.good_data = []
    self.bad_data = []
    for audio in os.listdir(good_dir):
        self.good_data.append(extract_features(os.path.join(good_dir, audio)))

    for audio in os.listdir(bad_dir):
        self.bad_data.append(extract_features(os.path.join(bad_dir, audio)))

    self.data = self.good_data + self.bad_data
    self.labels = [1] * sum(map(len, self.good_data)) + [0] * sum(map(len, self.bad_data))

    self.GMM_good = GaussianMixture(n_components=5, covariance_type='full', n_init=3, max_iter=1000, tol=1e-4)
    self.GMM_good.fit(np.concatenate(self.good_data))

    self.GMM_bad = GaussianMixture(n_components=5, covariance_type='full', n_init=3, max_iter=1000, tol=1e-4)
    self.GMM_bad.fit(np.concatenate(self.bad_data))

    self.kNN = KNeighborsClassifier(algorithm="kd_tree")
    self.kNN.fit(np.concatenate(self.data), self.labels)

  def label(self, audio):
    feat = extract_features(audio)
    
    prediction = self.kNN.predict(feat)
    good_count = sum(prediction)
    bad_count = len(prediction) - good_count
    print(good_count - bad_count)
      
    gscore = self.GMM_good.score(feat)
    bscore = self.GMM_bad.score(feat)

    score = gscore - bscore

    print(score)

    return 'good' if score > 0 else 'bad'