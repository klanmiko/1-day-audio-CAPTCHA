# 1-day-audio-CAPTCHA

The purpose of this project is to demonstrate the feasibility of using an audio based CATPCHA to distinguish between humans and bots.

## Authors
- Andrei Blebea - The-Boogeyman, NotDirectorofKGB
- Kaelan Mikowicz - klanmiko
- Kamal Sadek - Kamal-Sadek
- Monisha Ravindar - mravindar

## Main files

There are various scripts that are included in the project. The relevant ones are listed below.

app.py:
  - This is the Flask main server file that gets called with recorded audio data from the user.
  - Used to generate CAPTCHA text, load user response and check for correctness.
  - Run with ```flask run```.

server.js:
  - A node.js version of the server.

results.py:
  - Generates the results of running through all the testing audio samples.
  - For each audio testing sample, shows the number of matching human and bot frames.

preprocessing.py:
  - Contains helper functions used in the preprocessing of input audio files.

model.py:
  - Structure for training the relevant models (GMM, KNN, etc.) for the project.

stitch_attack.py:
  - Stitches together words in an attempt to fool the classifier.

stitch_attack2.py:
  - A slightly more advanced attack which after stitching together words attempts to smooth out the audio file and remove excessive silence to make it more convincing.

stitch_sniffer.py:
  - Proof of concept script that attempts to detect whether an audio file has been stitched together.

pca.py pca3.py:
  - Generates graphs that show a PCA of the model.

## Requirements
Python 3 is the required version for this project.

The requirements.txt should include all the Python libraries needed to run the scripts. You simply need to install them (preferrably through a virtual environment):
```
pip install -r requirements.txt (Windows)
pip3 install -r requirements.txt (Unix)
```

Additionally, there are a few system-wide packages that need to be installed. These are tkinter, festival, sox, and the Opus libraries (both the base package and the files package). If running in Ubuntu, the libraries can be installed with
```
sudo apt install python3-tk libopus-dev libopusfile-dev festival sox
```

It is recommended to run the Flask server in Development mode, so debugging is easier. This is done via:
```
set FLASK_ENV=development (Windows)
export FLASK_ENV=development (Unix)
```

Running the flask server is done with the command:
```
flask run
```

All of the other files are simply run as Python scripts:
```
python3 <script>
```
