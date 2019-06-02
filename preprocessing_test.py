import numpy as np
import array
import matplotlib.pyplot as plt

from pydub import AudioSegment
from itertools import zip_longest

import pdb

AUDIO_FILE = 'dataset/train/good/kaelan.wav'

def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

sound = AudioSegment.from_file(AUDIO_FILE)

samples = sound.get_array_of_samples()

result = []

for sample in grouper(1000, samples, 0):
    if abs(np.mean(sample)) > 50:
        result += list(sample)

result = array.array(sound.array_type, result)

print(len(result))
print(len(samples))

new_sound = sound._spawn(result)
new_sound.export('test_new.wav', format='wav')

new_sound = sound._spawn(samples)
new_sound.export('test_sound.wav', format='wav')

plt.plot(samples)
plt.show()

#pdb.set_trace()

