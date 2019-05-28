from flask import Flask, render_template, request
import pyogg
import audioop
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from model import Model
import os
import wave
import array

from captcha_gen.generator import generate_captcha

app = Flask(__name__)
model = Model()
model.train()

@app.route("/")
def index():
  text = generate_captcha()
  return render_template('index.html', captcha=text)

@app.route('/audio', methods=['POST'])
def audio():
    speech = request.files['speech']
    speech.save('./speech.ogg')
    opus = pyogg.OpusFile('./speech.ogg')

    a = array.array('h')
    for i in range(int(opus.buffer_length / 2)):
      a.append(opus.buffer[i])

    with wave.open('./speech.wav', 'wb') as writer:
      writer.setnchannels(opus.channels)
      writer.setframerate(opus.frequency)
      writer.setnframes(opus.buffer_length)
      writer.setsampwidth(2)
      writer.writeframesraw(a)

    with wave.open('./speech.wav', 'rb') as reader:
      print(reader.getparams())
    return app.make_response(model.label('./speech.wav'))