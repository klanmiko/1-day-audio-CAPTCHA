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

import speech_recognition as sr

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
    for i in range(int(opus.buffer_length / 2)): # pyogg doubles it for some reason
      a.append(opus.buffer[i])

    OUTPUT_FILE = './speech.wav'

    with wave.open(OUTPUT_FILE, 'wb') as writer:
      writer.setnchannels(opus.channels)
      writer.setframerate(opus.frequency)
      writer.setnframes(opus.buffer_length)
      writer.setsampwidth(2)
      writer.writeframesraw(a)

    r = sr.Recognizer()
    with sr.AudioFile(OUTPUT_FILE) as source:
        audio = r.record(source)
        print(r.recognize_sphinx(audio))

    return app.make_response(model.label('./speech.wav'))
