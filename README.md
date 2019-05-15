# 1-day-audio-CAPTCHA

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