import numpy
import scipy
import scipy.io.wavfile
import os
import fnmatch
import sys
import matplotlib.pyplot as plt

FREQUENCY = 44100

text = input("Enter words to generate: ")
textarr = text.split()
print(text)

sound = numpy.zeros((0, 2), dtype = numpy.int16)

for word in textarr:
	# search for file
	for file in os.listdir("words"):
		if fnmatch.fnmatch(file, word + "_*.wav"):
			os.system("cp words/" + file + " __tempfile.wav")
			break
		else:
			# not found: generate
			os.system("echo " + word + " | text2wave -scale 2 -o __tempfile.wav >/dev/null 2>&1")

	# either case: shift frequency
	os.system("sox -S __tempfile.wav __tempfile2.wav rate -L -s " + str(FREQUENCY) + " >/dev/null 2>&1")

	# read file
	rate, data = scipy.io.wavfile.read("__tempfile2.wav")

	# if one channel, duplicate
	if len(data.shape) != 2:
		data = numpy.column_stack((data, data))

	# append to sound
	sound = numpy.append(sound, data, axis=0)

	# cleanup if generated
	os.system("rm -f __tempfile.wav __tempfile2.wav")

sound = sound.astype(numpy.int16)

# write to output
fname = "stitched"
scipy.io.wavfile.write(fname + ".wav", FREQUENCY, sound)
os.system("aplay " + fname + ".wav")

plt.plot(sound[:, 1])
plt.show()
