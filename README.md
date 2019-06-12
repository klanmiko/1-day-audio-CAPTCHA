# 1-day-audio-CAPTCHA

## Authors
Andrei Blebea - The-Boogeyman, NotDirectorofKGB
Kaelan Mikowicz - klanmiko
Kamal Sadek - Kamal-Sadek
Monisha Ravindar - mravindar

## Main files

app.py:
  - This is the main server file that gets called with recorded audio data from the user
  - Used to generate CAPTCHA text, load user response and check for correctness

server.js:
  - Backup node.js version of the server in case python doesn't work out for us

## Install

Make and load a virtualenv if you want one

```
pip install -r requirements.txt (Windows)
pip3 install -r requirements.txt (Unix)
```

## Running

```
set FLASK_ENV=development (Windows)
export FLASK_ENV=development (Unix)
flask run
```

## Requirements
The requirements.txt should include all the Python libraries needed to run the scripts. You simply need to install them (preferrably throught a virtual environment):
```
pip install -r requirements.txt
```

Additionally, there are a few systemwide packages that need to be installed. These are tkinter, festival, sox, and the Opus libraries (both the base package and the files package). If running in Ubuntu, the libraries can be installed with
```
sudo apt install python3-tk libopus-dev libopusfile-dev festival sox
```
