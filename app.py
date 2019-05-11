from flask import Flask, send_file, request
import pyogg
import audioop
app = Flask(__name__)

@app.route("/")
def index():
    return send_file('./index.html')

@app.route('/audio', methods=['POST'])
def audio():
    speech = request.files['speech']
    speech.save('./speech.ogg')
    opus = pyogg.OpusFile('./speech.ogg')
    print(opus.buffer_length)
    cross = audioop.cross(opus.buffer, 1)
    print(cross)
    return app.make_response('')