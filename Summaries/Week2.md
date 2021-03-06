#Week 2 Meeting Notes
##Group: 1-Day (Andrei Blebea, Kaelan Mikowicz, Kamal Sadek, Monisha Selvanayagam Ravindar)

Group Update:

Andrei Blebea
* Last week: Looked into using MFCC audio features to classify voice samples. Effectiveness is questionable, but seems to work sometimes. Looked into basic classification methods.
* This week: Look into pitch tracking. Possibly normalize samples based on pitch. Possibly look for structural indicators of artificial voice.
* Issues: MFCC seems fairly chaotic i.e. different audio samples from the same person may seem very different.

Kaelan Mikowicz
* Last week: Wrote a simple flask server that is able to record and save a user's voice from a web page. Discovered ASVspoof and using GMM implementation on MFCC features.
* This week: Integrate captcha generation from Monisha, test combinations of machine learning + feature extraction
* Issues: Understanding how GMM works, finding libraries that can do the ML heavy lifting.

Kamal Sadek
* Last week: Researched papers audio CAPTCHA papers, and helped implement the proof of concepts for various algorithms.
* This week: Developed the MFCC model that extracts coefficients from an audio sample, and then uses closest neighbors to compare that sample to known human and bot speech, and based on the closest neighbor categorizes the input.
* Issues: Getting enough data for the closest neighbors algorithm.

Monisha Selvanayagam Ravindar
* Last week: I worked on generating random captcha phrases.
* This week: More efficient way of generating phrases, collect more data for bot vs human speech 
* Issues: I need to use a different method in obtaining random words from the dictionary. The open source library I'm using generates very obscure words, and the filtering options provided do not work sufficiently.

Trello: https://trello.com/b/mahKWlUO/ecs-153-final-project

Github: https://github.com/klanmiko/1-day-audio-CAPTCHA

https://github.com/klanmiko/1-day-audio-CAPTCHA/invitations
