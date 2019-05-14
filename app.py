from flask import Flask, send_file, request
import pyogg
import audioop
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route("/")
def index():
    return send_file('./index.html')

@app.route('/audio', methods=['POST'])
def audio():
    speech = request.files['speech']
    speech.save('./speech.ogg')
    opus = pyogg.OpusFile('./speech.ogg')
    cross = audioop.cross(opus.buffer, 1)
    print(opus.buffer_length)
    buffer = np.ctypeslib.as_array(opus.buffer, shape=(1000,))
    print(buffer)
    f, t, Sxx = signal.spectrogram(buffer, 100)
    plt.pcolormesh(t, np.fft.fftshift(f), np.fft.fftshift(Sxx, axes=0))
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    print(cross)
    return app.make_response('')