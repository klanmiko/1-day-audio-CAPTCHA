import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process

import pdb
import os

from python_speech_features import mfcc, logfbank, delta
from scipy.spatial import distance
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve

from scipy.optimize import brentq
from scipy.interpolate import interp1d

from sklearn import metrics

from sklearn.mixture import GaussianMixture

from sklearn.model_selection import StratifiedKFold

from preprocessing_test import remove_silence

good_dir = os.path.join(os.path.curdir, "dataset", "train", "good")
bad_dir = os.path.join(os.path.curdir, "dataset","train", "bad")

def extract_features(audio):
  sound = remove_silence(audio)
  (rate, sig) = wav.read(sound)
  features = mfcc(sig, rate, nfft=1024, preemph=0.97)
  d = delta(features, 2)
  dd = delta(d, 2)
  return list(map(lambda x, y, z: x + y + z, features, d, dd))

class Model():
  def evaluate(self):
    files = []
    labels = []
    features = {}
    for audio in os.listdir(good_dir):
        files.append(os.path.join(good_dir, audio))
        labels.append(1)

    for audio in os.listdir(bad_dir):
        files.append(os.path.join(bad_dir, audio))
        labels.append(0)

    
    skf = StratifiedKFold(n_splits=5, shuffle=True)
    kNN_scores = []
    kNN_recall = []

    gmm_specificity = []
    gmm_recall = []

    for train, test in skf.split(files, labels):
      good_data = []
      bad_data = []
      train_labels = []

      GMM_good = GaussianMixture(n_components=256, covariance_type='full', max_iter=200, tol=1e-3)
      GMM_bad = GaussianMixture(n_components=256, covariance_type='full', max_iter=200, tol=1e-3)

      kNN = KNeighborsClassifier(algorithm="kd_tree")

      for f in train:
        if files[f] not in features:
          features[files[f]] = extract_features(files[f])
        feat = features[files[f]]
        if labels[f] == 1:
          good_data.append(feat)
        else:
          bad_data.append(feat)
        
        train_labels += [labels[f]] * len(feat)

      GMM_good.fit(np.concatenate(good_data))
      GMM_bad.fit(np.concatenate(bad_data))

      kNN.fit(np.concatenate(good_data + bad_data), train_labels)

      gmm_scores = []
      l = []

      for f in train:
        feat = features[files[f]]
        gscore = GMM_good.score(feat)
        bscore = GMM_bad.score(feat)
        gmm_scores.append(gscore - bscore)
        l.append(labels[f])

      fpr, tpr, thresholds = roc_curve(l, gmm_scores)
      eer = brentq(lambda x : 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
      thresh = interp1d(fpr, thresholds)(eer)

      test_data = []
      test_labels = []
      gmm_predictions = []
      predictions = []
      gmm_scores = []

      for f in test:
        if files[f] not in features:
          features[files[f]] = extract_features(files[f])
        feat = features[files[f]]
        test_data.append(feat)
        test_labels.append(labels[f])
        gscore = GMM_good.score(feat)
        bscore = GMM_bad.score(feat)
        gmm_predictions.append(0 if gscore - bscore < thresh else 1)
        gmm_scores.append(gscore - bscore)
        p = kNN.predict(feat)
        g_count = sum(p)
        b_count = len(p) - sum(p)
        predictions.append(1 if b_count == 0 or g_count / b_count > 3.5 else 0)
      
      tn, fp, fn, tp = metrics.confusion_matrix(test_labels, predictions).ravel()
      specificity = tn / (tn+fp)
      recall = tp / (tp + fn)
      kNN_scores.append(specificity)
      kNN_recall.append(recall)

      tn, fp, fn, tp = metrics.confusion_matrix(test_labels, gmm_predictions).ravel()
      specificity = tn / (tn+fp)
      recall = tp / (tp + fn)
      gmm_specificity.append(specificity)
      gmm_recall.append(recall)

    avg_knn = np.array(kNN_scores).mean()
    avg_knn_recall = np.array(kNN_recall).mean()
    print("knn specificity: ", avg_knn)
    print("knn recall: ", avg_knn_recall)

    avg_knn = np.array(gmm_specificity).mean()
    avg_knn_recall = np.array(gmm_recall).mean()
    print("gmm specificity: ", avg_knn)
    print("gmm recall: ", avg_knn_recall)

  def train(self):
    self.good_data = []
    self.bad_data = []
    self.labels = []
    feature_dict = {}

    for audio in os.listdir(good_dir):
        features = extract_features(os.path.join(good_dir, audio))
        feature_dict[audio] = features
        self.good_data.append(features)

    for audio in os.listdir(bad_dir):
        features = extract_features(os.path.join(bad_dir, audio))
        feature_dict[audio] = features
        self.bad_data.append(features)

    self.data = self.good_data + self.bad_data
    self.labels = [1] * sum(map(len,self.good_data)) + [0] * sum(map(len, self.bad_data))

    self.fnames = os.listdir(good_dir)
    self.fnames = self.fnames + os.listdir(bad_dir)

    print("training GMMs")    

    self.GMM_good = GaussianMixture(n_components=256, covariance_type='full', max_iter=100, tol=1e-3)
    #self.GMM_good.fit(np.concatenate(self.good_data))

    self.GMM_bad = GaussianMixture(n_components=256, covariance_type='full', max_iter=100, tol=1e-3)
    #self.GMM_bad.fit(np.concatenate(self.bad_data))

    # regression_data = []
    # regression_labels = []

    # for audio in os.listdir(good_dir):
    #     features = feature_dict[audio]
    #     gscore = self.GMM_good.score(features)
    #     bscore = self.GMM_bad.score(features)
    #     regression_data.append(gscore - bscore)
    #     regression_labels.append(1)

    # for audio in os.listdir(bad_dir):
    #     features = feature_dict[audio]
    #     gscore = self.GMM_good.score(features)
    #     bscore = self.GMM_bad.score(features)
    #     regression_data.append(gscore - bscore)
    #     regression_labels.append(0)

    # fpr, tpr, thresholds = roc_curve(regression_labels, regression_data, drop_intermediate=False)
    
    # eer = brentq(lambda x : 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
    # self.thresh = interp1d(fpr, thresholds)(eer)
    # print("threshold: ", self.thresh)

    print("Loading kNN")

    self.kNN = KNeighborsClassifier(algorithm="kd_tree", n_neighbors=8)
    self.kNN.fit(np.concatenate(self.data), self.labels)

  def plot(self, audio, matches):
    try:
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
    except Exception as e:
      print(e)

  def label(self, audio):
    feat = extract_features(audio)
    
    prediction = self.kNN.predict(feat)
    
    good_count = sum(prediction)
    bad_count = len(prediction) - good_count

    print("good_count: ", good_count)
    print("bad_count: ", bad_count)
      
    # gscore = self.GMM_good.score(feat)
    # bscore = self.GMM_bad.score(feat)

    # print("gscore: ", gscore)
    # print("bscore: ", bscore)

    # score = gscore - bscore

    return 'good' if bad_count == 0 or good_count / bad_count > 3.5 else 0