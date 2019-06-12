import os
import pdb

import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np

from python_speech_features import mfcc
from scipy.spatial import distance, KDTree
from preprocessing import remove_silence

def extract_features(audio):
    sound = remove_silence(audio)
    (rate, sig) = wav.read(sound)
    features = mfcc(sig, rate, nfft=1024, preemph=0.9)
    return features

human_training_dir = os.path.join(os.path.curdir, 'dataset', 'train', 'good')
bot_training_dir = os.path.join(os.path.curdir, 'dataset', 'train', 'bad')

human_testing_dir = os.path.join(os.path.curdir, 'dataset', 'human')
bot_testing_dir = os.path.join(os.path.curdir, 'dataset', 'bot')

human_data = np.empty(shape=(0, 13))
bot_data = np.empty(shape=(0, 13))

for human_audio in os.listdir(human_training_dir):
    features = extract_features(os.path.join(human_training_dir, human_audio))
    human_data = np.concatenate((human_data, features))

for bot_audio in os.listdir(bot_training_dir):
    features = extract_features(os.path.join(bot_training_dir, bot_audio))
    bot_data = np.concatenate((bot_data, features))

tree = KDTree(np.concatenate((human_data, bot_data)))

human_count = 0
bot_count = 0

human_count_per = []
bot_count_per = []
files = []

for human_test_audio in os.listdir(human_testing_dir):
    files.append(human_test_audio)
    print(human_test_audio)
    human_count_pre = human_count
    bot_count_pre = bot_count
    for feature in extract_features(os.path.join(human_testing_dir, human_test_audio)):
        (dist, ind) = tree.query(feature)
        if ind < len(human_data):
            human_count += 1
        else:
            bot_count += 1
    human_count_per.append(human_count - human_count_pre)
    bot_count_per.append(bot_count - bot_count_pre)

pdb.set_trace()

print(files)
print(human_count_per)
print(bot_count_per)
print(human_count, bot_count)
