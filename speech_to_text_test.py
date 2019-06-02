import speech_recognition as sr

AUDIO_FILE='dataset/train/good/kaelan.wav'

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)

print(r.recognize_sphinx(audio))
