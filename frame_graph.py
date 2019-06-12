import os
import pickle
import pdb

import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

from python_speech_features import mfcc
from scipy.spatial import distance, KDTree
from preprocessing_test import remove_silence

human_training_dir = os.path.join(os.path.curdir, 'dataset', 'train', 'good')
bot_training_dir = os.path.join(os.path.curdir, 'dataset', 'train', 'bad')

def extract_features(audio):
    sound = remove_silence(audio)
    (rate, sig) = wav.read(sound)
    features = mfcc(sig, rate, nfft=1024, preemph=0.9)
    return features

human_data = np.empty(shape=(0, 13))
bot_data = np.empty(shape=(0, 13))

for human_audio in os.listdir(human_training_dir):
    features = extract_features(os.path.join(human_training_dir, human_audio))
    human_data = np.concatenate((human_data, features))

for bot_audio in os.listdir(bot_training_dir):
    features = extract_features(os.path.join(bot_training_dir, bot_audio))
    bot_data = np.concatenate((bot_data, features))

tree = KDTree(np.concatenate((human_data, bot_data)))

human_data_dump = pickle.dumps(human_data)
bot_data_dump = pickle.dumps(bot_data)
tree_dump = pickle.dumps(tree)

human_files = ['shrink_next_door.wav', 'the_daily.wav']
bot_files = ['bot4.wav', 'bot5.wav']#'google1.wav', 'cortana.wav']

files = np.concatenate((human_files, bot_files))

human_count_per = []
bot_count_per = []

for audio in human_files:
    human_count = 0
    bot_count = 0
    for feature in extract_features(os.path.join(os.path.curdir, 'dataset', 'human', audio)):
        (dist, ind) = tree.query(feature)
        if ind < len(human_data):
            human_count += 1
        else:
            bot_count += 1
    human_count_per.append(human_count)
    bot_count_per.append(bot_count)

for audio in bot_files:
    human_count = 0
    bot_count = 0
    for feature in extract_features(os.path.join(os.path.curdir, 'dataset', 'bot', audio)):
        (dist, ind) = tree.query(feature)
        if ind < len(human_data):
            human_count += 1
        else:
            bot_count += 1
    human_count_per.append(human_count)
    bot_count_per.append(bot_count)

N = len(files)
ind = np.arange(N)
width = 0.35

p1 = plt.bar(ind, human_count_per)
p2 = plt.bar(ind, bot_count_per)

plt.title('Number of Human vs Bot Frames per Sample')
plt.ylabel('Number of Frames')
plt.xticks(ind, ['Human 1', 'Human 2', 'Bot 1', 'Bot 2'])
plt.legend((p1[0], p2[0]), ('Human Frames', 'Bot Frames'))

plt.show()

pdb.set_trace()
