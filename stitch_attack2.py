import numpy
import scipy
import scipy.io.wavfile
import os
import fnmatch
import sys
import matplotlib.pyplot as plt

# now removes noise/blends words together

FREQUENCY = 44100
OVERLAP = 5000

text = input("Enter words to generate: ")
textarr = text.split()
print(text)

sound = numpy.zeros((0, 2), dtype = numpy.int16)

first = True

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

	# remove silence
	os.system("sox __tempfile2.wav __tempfile3.wav silence -l 1 0 1% -1 0 1%")

	# read file
	rate, data = scipy.io.wavfile.read("__tempfile3.wav")

	# if one channel, duplicate
	if len(data.shape) != 2:
		data = numpy.column_stack((data, data))

	# append to sound
	if first:
		sound = numpy.append(sound, data, axis=0)
		first = False
	else:
		lb = sound.shape[0] - OVERLAP
		for i in range(OVERLAP - 1):
			sound[lb + i, :] = numpy.add(numpy.multiply(sound[lb + i, :], float(OVERLAP - i)/OVERLAP), numpy.multiply(data[i, :], float(i)/OVERLAP))
		sound = numpy.append(sound, data[OVERLAP:, :], axis=0)
			
	# cleanup if generated
	os.system("rm -f __tempfile.wav __tempfile2.wav __tempfile3.wav")

sound = sound.astype(numpy.int16)

# plot
plt.figure(1)
plt.plot(sound[:, 0])
plt.draw()

# write to output
fname = "stitched"
scipy.io.wavfile.write(fname + ".wav", FREQUENCY, sound)
os.system("aplay " + fname + ".wav")

plt.show()
