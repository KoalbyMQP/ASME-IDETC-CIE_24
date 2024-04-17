# Very basic TTS (text-to-speech example)

import pyttsx3
engine = pyttsx3.init()

# set female voice
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)

# Run
engine.say("Hi, my name is Ava! How can I help you today?")
engine.runAndWait()