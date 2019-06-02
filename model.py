import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np
import threading

import pdb
import os

from python_speech_features import mfcc, logfbank, delta
from scipy.spatial import distance
from sklearn.neighbors import KNeighborsClassifier

from sklearn.mixture import GaussianMixture

from preprocessing_test import remove_silence

good_dir = os.path.join(os.path.curdir, "dataset", "train", "good")
bad_dir = os.path.join(os.path.curdir, "dataset","train", "bad")

def extract_features(audio):
  sound = remove_silence(audio)
  (rate, sig) = wav.read(sound)
  features = mfcc(sig, rate, nfft=1024, preemph=0.9)
  d = delta(features, 2)
  return list(map(lambda x, y: x + y, features, d))

class Model():
  def train(self):
    self.good_data = []
    self.bad_data = []
    self.labels = []
    self.l_count = 0
    for audio in os.listdir(good_dir):
        features = extract_features(os.path.join(good_dir, audio))
        self.good_data.append(features)
        self.labels += ([self.l_count] * len(features))
        self.l_count += 1

    self.cutoff = self.l_count

    for audio in os.listdir(bad_dir):
        features = extract_features(os.path.join(bad_dir, audio))
        self.bad_data.append(features)
        self.labels += ([self.l_count] * len(features))
        self.l_count += 1

    self.data = self.good_data + self.bad_data

    self.fnames = os.listdir(good_dir)
    self.fnames = self.fnames + os.listdir(bad_dir)

    print("training GMMs")    

    self.GMM_good = GaussianMixture(n_components=50, covariance_type='full', n_init=2, max_iter=200, tol=1e-4)
    self.GMM_good.fit(np.concatenate(self.good_data))

    self.GMM_bad = GaussianMixture(n_components=50, covariance_type='full', n_init=2, max_iter=200, tol=1e-4)
    self.GMM_bad.fit(np.concatenate(self.bad_data))

    print("Loading kNN")

    self.kNN = KNeighborsClassifier(algorithm="kd_tree")
    self.kNN.fit(np.concatenate(self.data), self.labels)

  def plot(self, audio, matches):
    feat = extract_features(audio)

    plt.subplot(2,2,1)
    plt.plot(feat)
    plt.title("Sample")
    ind = 2
    titles = ["Closest Match", "Middle Match", "Furthest Match"]
    for i in [0, int(len(matches)/2), len(matches) - 1]:
      name = matches[i]
      if name in os.listdir(good_dir):
        feat = extract_features(os.path.join(good_dir, name))
      else:
        feat  = extract_features(os.path.join(bad_dir, name))
      plt.subplot(2,2,ind)
      plt.plot(feat)
      plt.title(titles[ind  - 2])
      ind = ind + 1
    
    plt.show()

  def label(self, audio):
    feat = extract_features(audio)
    
    prediction = self.kNN.predict(feat)
    
    good_count = len([i for i in prediction if i < self.cutoff])
    bad_count = len(prediction) - good_count

    mapping = [0] * self.l_count
    for i in prediction:
      mapping[i] += 1

    print(mapping)
    print("good_count: ", good_count)
    print("bad_count: ", bad_count)

    count = good_count - bad_count
      
    gscore = self.GMM_good.score(feat)
    bscore = self.GMM_bad.score(feat)

    print("gscore: ", gscore)
    print("bscore: ", bscore)

    matches = [x for _, x in sorted(zip(mapping, self.fnames), reverse=True)]
    print("Ordered matches: ")
    print(matches)

    t1 = threading.Thread(target=self.plot, args=(self, audio, matches)) 

    score = gscore - bscore

    print(score)

    return 'good' if count > 10 else 'bad'