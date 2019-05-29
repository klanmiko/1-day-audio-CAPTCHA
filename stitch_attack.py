import numpy
import scipy
import scipy.io.wavfile
import os
import fnmatch

text_as_wav = lambda text, frequency : print("echo " + text + " | text2wave -scale 2 -o __tempfile.wav; sox -S __tempfile.wav __tempfile2.wav rate -L -s " + str(frequency))

os.system("echo hello")
text_as_wav("hello there", 44100)

rate1, data1 = scipy.io.wavfile.read("Matlab_Attempt/hal.wav")
rate2, data2 = scipy.io.wavfile.read("Matlab_Attempt/bootleg.wav")

if rate1 != rate2:
	print("Rate error")

data3 = numpy.append(data1, data2, axis=0)

scipy.io.wavfile.write("TEMP.wav", rate1, data3);
