import numpy
import scipy
import scipy.io.wavfile
import os
import fnmatch
import sys
import matplotlib.pyplot as plt
from python_speech_features import mfcc


NOISETHRESHOLD = 1000

fname = input("Enter name of file to test: ")

rate, data = scipy.io.wavfile.read(fname)

size = data.shape[0]

slist = []
clist = []
cbuf = []
blist = []
elist = []

length = 0
index = 0

print(size)

step = 20

for i in range(0, size-1, step):
	if i % (step * 100) == 0:
		print(i)

	if abs(data[i, 0]) < NOISETHRESHOLD:
		cbuf = cbuf + ["r"]
	else:
		# long silence
		if len(cbuf) > rate/(3*step):
			blist.insert(index, i - len(cbuf)*step)
			elist.insert(index, i) 
			clist = clist + cbuf
			slist.insert(index, step*len(cbuf)/rate)
			index = index + 1
		else:
			clist = clist + ["g"]*len(cbuf)
		cbuf = []
		clist = clist + ["g"]

clist = clist + cbuf
blist.insert(index, i - len(cbuf)*step)
elist.insert(index, i)
slist.insert(index, step*len(cbuf)/rate)


print(slist)
print(len(clist))

soundlist = []
index = 0

if blist[0] != 0:
	soundlist.insert(index, data[0:blist[0], 0])
	index = index + 1

for i in range(len(elist) - 1):
	soundlist.insert(index, data[elist[i]:blist[i+1], 0])
	index = index + 1

for i in range(len(soundlist)):
	print(i)
	s = soundlist[i]
	f = plt.figure()
	f.canvas.set_window_title('Mfcc for sound region ' + str(i))
	plt.plot(mfcc(s, rate, nfft = 1103))
	plt.show(block = False)

fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(0, size-1, step):
	if i % (step * 100) == 0:
                print(i)

	ax.scatter(i, data[i,0], color= clist[int(i/step)], s=1)

plt.show()
