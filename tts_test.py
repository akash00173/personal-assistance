import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("Available voices:")
for i, voice in enumerate(voices):
    print(i, voice.name, voice.id)

engine.setProperty('voice', voices[0].id)  # try first voice
engine.setProperty('rate', 170)

engine.say("Hello, this is a test of your text to speech engine.")
engine.runAndWait()
