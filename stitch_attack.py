import numpy
import scipy
import scipy.io.wavfile
import os

os.system("echo hello")

rate1, data1 = scipy.io.wavfile.read("Matlab_Attempt/hal.wav")
rate2, data2 = scipy.io.wavfile.read("Matlab_Attempt/bootleg.wav")

if rate1 != rate2:
	print("Rate error")

data3 = numpy.append(data1, data2, axis=0)

scipy.io.wavfile.write("TEMP.wav", rate1, data3);
