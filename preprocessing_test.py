import numpy as np
import array
import matplotlib.pyplot as plt

from pydub import AudioSegment
from itertools import zip_longest

import pdb

#AUDIO_FILE = 'dataset/train/good/andre.wav'

def remove_silence(AUDIO_FILE):
    def grouper(n, iterable, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(fillvalue=fillvalue, *args)

    sound = AudioSegment.from_file(AUDIO_FILE)

    samples = sound.get_array_of_samples()

    result = []

    for sample in grouper(10000, samples, 0):
        if np.mean(np.abs(sample)) > 300:
            result += list(sample)

    result = array.array(sound.array_type, result)

    new_sound = sound._spawn(result)
    new_sound.export('test_new.wav', format='wav')
    return 'test_new.wav'

# plt.subplot(2,1,2)
# plt.plot(new_sound.get_array_of_samples())

# new_sound = sound._spawn(samples)
# new_sound.export('test_sound.wav', format='wav')

# plt.subplot(2,1,1)
# plt.plot(new_sound.get_array_of_samples())

# plt.show()

# #pdb.set_trace()

