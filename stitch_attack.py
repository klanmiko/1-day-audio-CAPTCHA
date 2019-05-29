import numpy
import scipy
import scipy.io.wavfile
import os
import fnmatch
import sys

FREQUENCY = 44100

text = input("Enter words to generate: ")
textarr = text.split()
print(text)

sound = numpy.zeros((0, 2), dtype = numpy.int16)

stdout = sys.stdout
dnull = open(os.devnull, 'w')
stdout = sys.stdout
stderr = sys.stderr
sys.stdout = dnull
sys.stderr = dnull

for word in textarr:
	# search for file
	
	# not found: generate
	os.system("echo " + word + " | text2wave -scale 2 -o __tempfile.wav >/dev/null 2>&1")

	# either case: shift frequency
	os.system("sox -S __tempfile.wav __tempfile2.wav rate -L -s " + str(FREQUENCY) + " >/dev/null 2>&1")

	# read file
	rate, data = scipy.io.wavfile.read("__tempfile2.wav")
	print("========================================================")
	print(sound.shape)
	print(data.shape)
	print(data[1:20])
	print("========================================================")

	# if one channel, duplicate
	if len(data.shape) != 2:
		data = numpy.column_stack((data, data))
	print(data.shape)

	# append to sound
	sound = numpy.append(sound, data, axis=0)

	print(sound[1:30, :])

	# cleanup if generated
#	os.system("rm -f __tempfile.wav __tempfile2.wav")

sys.stderr = stderr
sys.stdout = stdout

sound = sound.astype(numpy.int16)

# write to output
fname = "stitched"
print(fname + ".wave")
scipy.io.wavfile.write(fname + ".wav", FREQUENCY, sound)
# play sound?
os.system("aplay " + fname + ".wav")


#text_as_wav = lambda text, frequency : print("echo " + text + " | text2wave -scale 2 -o __tempfile.wav; sox -S __tempfile.wav __tempfile2.wav rate -L -s " + str(frequency))

#os.system("echo hello")
#text_as_wav("hello there", 44100)

#rate1, data1 = scipy.io.wavfile.read("Matlab_Attempt/hal.wav")
#rate2, data2 = scipy.io.wavfile.read("Matlab_Attempt/bootleg.wav")

#print("shape")
#print(data1.shape)

#if rate1 != rate2:
#	print("Rate error")

#data3 = numpy.append(data1, data2, axis=0)

#scipy.io.wavfile.write("TEMP.wav", rate1, data3)
